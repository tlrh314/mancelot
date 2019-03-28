#!/usr/bin/env bash

set -e

DATA_PATH="./data/certbot"
EMAIL="info@mancelot.nl"
RSA_KEY_SIZE=4096

# Select appropriate EMAIL arg
case "$EMAIL" in
  "") EMAIL_ARG="--register-unsafely-without-email" ;;
  *) EMAIL_ARG="--email $EMAIL" ;;
esac

# Obtain options-ssl-nginx.conf and ssl-dhparams.pem from certbot repo
if [ ! -e "${DATA_PATH}/conf/options-ssl-nginx.conf" ] || [ ! -e "${DATA_PATH}/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "${DATA_PATH}/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/options-ssl-nginx.conf > "${DATA_PATH}/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/ssl-dhparams.pem > "${DATA_PATH}/conf/ssl-dhparams.pem"
  echo
fi

# Make sure our container is at the latest version
docker-compose build

# Make sure nginx is running
echo "### Starting nginx ..."
docker-compose up --force-recreate -d nginx
echo

# Declare each domains and generate Let's Encrypt certificate
declare -a DOMAINS=(
    "mancelot.be"
    "mancelot.com"
    "mancelot.co.uk"
    "mancelot.de"
    "mancelot.eu"
    "mancelot.nl"
        "mm.mancelot.nl"
)

for DOMAIN in "${DOMAINS[@]}"
do
    echo "### Creating dummy certificate for $DOMAIN ..."
    LE_PATH="/etc/letsencrypt/live/$DOMAIN"
    mkdir -p "${DATA_PATH}/conf/live/$DOMAIN"  # Inside the container
    docker-compose run --rm --entrypoint "\
      openssl req -x509 -nodes -newkey rsa:1024 -days 1\
        -keyout '${LE_PATH}/privkey.pem' \
        -out '${LE_PATH}/fullchain.pem' \
        -subj '/CN=localhost'" certbot
    echo

    is_subdomain=false
    echo -e "\nDomain: $DOMAIN"
    ndots_when_subdomain=2
    if [[ $DOMAIN =~ ".co.uk" ]]; then
        ndots_when_subdomain=3
    fi

    dots="${DOMAIN//[^.]}"
    ndots=${#dots}
    if (( $ndots >= $ndots_when_subdomain )); then
        is_subdomain=true
    fi

    if $is_subdomain; then
        DOMAIN_ARGS="-d ${DOMAIN}"
    else
        DOMAIN_ARGS="-d ${DOMAIN} -d www.${DOMAIN}"
        if [[ $DOMAIN =~ "projectcece" ]]; then
            DOMAIN_ARGS="${DOMAIN_ARGS} -d staging.${DOMAIN}"
        fi
    fi

    echo "### Deleting dummy certificate for $DOMAIN ..."
    docker-compose run --rm --entrypoint "\
      rm -Rf /etc/letsencrypt/live/$DOMAIN && \
      rm -Rf /etc/letsencrypt/archive/$DOMAIN && \
      rm -Rf /etc/letsencrypt/renewal/$DOMAIN.conf" certbot
    echo

    echo "### Requesting Let's Encrypt certificate for $DOMAIN_ARGS ..."
    docker-compose run --rm --entrypoint "\
      certbot certonly --webroot -w /var/www/certbot \
        $EMAIL_ARG \
        $DOMAIN_ARGS \
        --rsa-key-size $RSA_KEY_SIZE \
        --agree-tos \
        --force-renewal" certbot
    echo
done

# And finally we reload our nginx container
echo "### Reloading nginx ..."
docker-compose exec nginx nginx -s reload
