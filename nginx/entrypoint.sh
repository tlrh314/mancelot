#!/bin/sh

# Define default value for app container hostname and port
MATTERMOST_HOST=${MATTERMOST_HOST:-mattermost}
MATTERMOST_PORT_NUMBER=${MATTERMOST_PORT_NUMBER:-8000}

# Check if SSL should be enabled (if certificates exists)
if [ -f "/cert/cert.pem" -a -f "/cert/key-no-password.pem" ]; then
  echo "found certificate and key, linking ssl config"
  ssl="-ssl"
else
  echo "linking plain config"
fi
# Linking Nginx configuration file
# ln -s /etc/nginx/sites-available/mattermost$ssl /etc/nginx/conf.d/mattermost.conf
ln -s /etc/nginx/sites-available/mancelot.nl.conf /etc/nginx/conf.d

# Setup app host and port on configuration file
# sed -i "s/{%MATTERMOST_HOST%}/${MATTERMOST_HOST}/g" /etc/nginx/conf.d/mattermost.conf
# sed -i "s/{%MATTERMOST_PORT%}/${MATTERMOST_PORT_NUMBER}/g" /etc/nginx/conf.d/mattermost.conf

# Run Nginx
# TODO? command: "/bin/sh -c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'"
exec nginx -g 'daemon off;'

