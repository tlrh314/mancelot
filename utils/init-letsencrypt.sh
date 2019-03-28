#!/usr/bin/env bash

set -e

DOMAINS=(mancelot.nl www.mancelot.nl)
RSA_KEY_SIZE=4096
DATA_PATH="./data/certbot"
EMAIL="info@mancelot.nl" # Adding a valid address is strongly recommended
STAGING=1 # Set to 1 if you're testing your setup to avoid hitting request limits

if [ -d "${DATA_PATH}" ]; then
  read -p "Existing data found for $DOMAINS. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi


if [ ! -e "${DATA_PATH}/conf/options-ssl-nginx.conf" ] || [ ! -e "${DATA_PATH}/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "${DATA_PATH}/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/options-ssl-nginx.conf > "${DATA_PATH}/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/ssl-dhparams.pem > "${DATA_PATH}/conf/ssl-dhparams.pem"
  echo
fi

echo "### Creating dummy certificate for $DOMAINS ..."
LE_PATH="/etc/letsencrypt/live/$DOMAINS"
mkdir -p "${DATA_PATH}/conf/live/$DOMAINS"  # Inside the container
docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:1024 -days 1\
    -keyout '${LE_PATH}/privkey.pem' \
    -out '${LE_PATH}/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo


echo "### Starting nginx ..."
docker-compose up --force-recreate -d nginx
echo

exit 0

echo "### Deleting dummy certificate for $DOMAINS ..."
docker-compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$DOMAINS && \
  rm -Rf /etc/letsencrypt/archive/$DOMAINS && \
  rm -Rf /etc/letsencrypt/renewal/$DOMAINS.conf" certbot
echo


echo "### Requesting Let's Encrypt certificate for $DOMAINS ..."
#Join $DOMAINS to -d args
DOMAIN_ARGS=""
for domain in "${DOMAINS[@]}"; do
  DOMAIN_ARGS="$DOMAIN_ARGS -d $domain"
done

# Select appropriate EMAIL arg
case "$EMAIL" in
  "") EMAIL_ARG="--register-unsafely-without-email" ;;
  *) EMAIL_ARG="--email $EMAIL" ;;
esac

# Enable staging mode if needed
if [ ${STAGING} != "0" ]; then STAGING_ARG="--staging --dry-run"; fi

docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $STAGING_ARG \
    $EMAIL_ARG \
    $DOMAIN_ARGS \
    --rsa-key-size $RSA_KEY_SIZE \
    --agree-tos \
    --force-renewal" certbot
echo

echo "### Reloading nginx ..."
docker-compose exec nginx nginx -s reload
