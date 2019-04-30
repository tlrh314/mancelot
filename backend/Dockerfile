FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

LABEL maintainer="Timo Halbesma <timo@mancelot.nl>"

# Install Alpine system packages
WORKDIR /mancelot
RUN set -ex \
    && apk upgrade --no-cache \
    \
    # virtual package w/ build dependencies
    && apk add --no-cache --virtual .build-deps \
        build-base \
        libffi-dev \
        linux-headers \
    \
    # Install Runtime dependencies ...
    && apk add --no-cache \
        # ... for a proper shell
        bash \
        # ... for the healthcheck
        curl \
        # ... for communication with the database
        mariadb-client mariadb-dev \
        # ... for Pillow
        jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    \
    # Create mancelot user to run uWSGI as non-root
    && addgroup -g 1000 -S mancelot \
    && adduser -u 1000 -S mancelot -G mancelot \
    && chown -R mancelot:mancelot /mancelot

# Install python packages for Django
COPY requirements.txt /mancelot/requirements.txt
RUN set -ex && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /mancelot/requirements.txt

# We're done installing, so remove the .build-deps virtual package
RUN set -ex && \
    apk del .build-deps && \
    rm -rf /root/.cache/ && \
    rm -rf /tmp/*

HEALTHCHECK --interval=5m --timeout=5s \
    CMD curl --fail http://localhost:8000 || exit 1

USER mancelot
