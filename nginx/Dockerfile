FROM nginx:1.19-alpine

LABEL maintainer="Timo Halbesma <timo@mancelot.app>"

# Remove the default configuration files
RUN set -ex \
    && apk add --no-cache curl bash htop \
    && rm /etc/nginx/conf.d/*

# Insert our own configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf/*.conf /etc/nginx/conf.d/
COPY apps/*.conf /etc/nginx/apps/

HEALTHCHECK --interval=2m --timeout=3s \
    CMD curl -I -k --fail -H "Host: mancelot.app" -k https://localhost || exit 1
