#!/usr/bin/env bash

set -e

# TODO: implement these functions as arguments
DATA_PATH="./data/certbot"
EMAIL="info@mancelot.nl"
RSA_KEY_SIZE=4096
PRODUCTION=false
case "$EMAIL" in
  "") EMAIL_ARG="--register-unsafely-without-email" ;;
  *) EMAIL_ARG="--email $EMAIL" ;;
esac

_usage() {
cat <<EOF
Usage: `basename $0` <options>

Build initial Docker container(s) w/ self-signed certs for development.
  For production: use -p (or --prod) to replace self-signed w/ Let's Encrypt certs

Options:
  -h   --help           display this help and exit
  -p   --prod           remove the self-signed SSL certificate; do call certbot

Examples:
  `basename $0` 
  `basename $0` --prod
EOF
}
parse_options() {
    # https://stackoverflow.com/questions/192249
    # It is possible to use multiple arguments for a long option.
    # Specifiy here how many are expected.
    declare -A longoptspec
    longoptspec=( )  # e.g. [use]=1 

    optspec="hp-:"
    while getopts "$optspec" opt; do
    while true; do
        case "${opt}" in
            -) # OPTARG is long-option or long-option=value.
                # Single argument:   --key=value.
                if [[ "${OPTARG}" =~ .*=.* ]]
                then
                    opt=${OPTARG/=*/}
                    OPTARG=${OPTARG#*=}
                    ((OPTIND--))
                # Multiple arguments: --key value1 value2.
                else
                    opt="$OPTARG"
                    OPTARG=(${@:OPTIND:$((longoptspec[$opt]))})
                fi
                ((OPTIND+=longoptspec[$opt]))
                # opt/OPTARG set, thus, we can process them as if getopts would've given us long options
                continue
                ;;
            h|help)
                _usage
                exit 0
                ;;
            p|prod)
                PRODUCTION=true
                ;;
        esac
    break; done
    done
}
parse_options $@


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
        "api.mancelot.nl"
        "mm.mancelot.nl"
        "pw.mancelot.nl"
)

for DOMAIN in "${DOMAINS[@]}"
do
    echo "### Checking content of Let's Encrypt live folder for $DOMAIN ..."

    folder="${DATA_PATH}/conf/live/$DOMAIN"
    if [ -f "${folder}/privkey.pem" ]; then
        # This means that at least our self-signed certificate is there
        echo "  Success: privkey.pem exists. Could be self-signed or Let's Encrypt."
        if [ "$PRODUCTION" = false ]; then
        echo -e "  This is production. We're done here.\n"
            continue
        fi
    fi

    if [ -f "${folder}/cert.pem" ]; then
        # This means that we already have our Let's Encrypt certificates
        echo -e "Success: cert.pem exists. We can continue.\n"
        continue
    fi

    echo "### Creating self-signed certificate for $DOMAIN ..."
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
        if [[ $DOMAIN =~ "mancelot.nl" ]]; then
            DOMAIN_ARGS="${DOMAIN_ARGS} -d staging.${DOMAIN}"
        fi
    fi

    if [ "$PRODUCTION" = false ]; then
        echo "PRODUCTION is false. We shall leave self-signed certs as-is."
        continue
    else
        echo "PRODUCTION is true. Call certbot to replace self-signed certs w/ Let's Encrypt certs."
    fi


    echo "### Deleting self-signed certificate for $DOMAIN ..."
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
