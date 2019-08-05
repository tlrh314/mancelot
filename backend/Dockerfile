FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED 1

LABEL maintainer="Timo Halbesma <timo@mancelot.nl>"

# Install Alpine system packages
WORKDIR /mancelot
RUN set -ex \
    && apt-get update \
\
    # Install Runtime dependencies ...
    && apt-get install -y --no-install-recommends \
\
        # ... a compiler
        build-essential gcc \
        # ... for a proper editor
        vim \
        # ... for the healthcheck
        curl \
        # ... for internal routing of uWSGI
        libpcre3 libpcre3-dev \
        # ... for communication with the database
        mariadb-client libmariadb-dev-compat \
\
    # Create mancelot user to run uWSGI as non-root
    && groupadd -g 1000 mancelot \
    && useradd -r -u 1000 -g mancelot mancelot -s /bin/bash -d /mancelot \
    && chown -R mancelot:mancelot /mancelot

# Install python packages for Django
COPY requirements.txt /mancelot/requirements.txt
RUN set -ex && \
    pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /mancelot/requirements.txt

USER mancelot
