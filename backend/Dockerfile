FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

LABEL maintainer="Timo Halbesma <timo@mancelot.nl>"

# Install Debian system packages
WORKDIR /mancelot
RUN set -ex \
    && apt-get update \
\
    # Install Build/Runtime dependencies ...
    && apt-get install -y --no-install-recommends \
\
        # ... a compiler (build)
        build-essential gcc \
        # ... for a proper editor (runtime)
        vim \
        # ... for the healthcheck (runtime)
        curl \
        # ... for monitoring (runtime)
        htop \
        # ... for Django translations (runtime)
        gettext \
        # ... for 'graph_models' (django-extensions) cmd to visualise db schema (runtime)
        graphviz graphviz-dev \
        # ... for internal routing of uWSGI (runtime)
        libpcre3 libpcre3-dev \
        # ... for communication with the database (runtime)
        mariadb-client libmariadb-dev-compat \
        # ... to optimize images
        jpegoptim optipng pngquant gifsicle \
        # if needed, add SVGO to optimize svg files: npm install -g svgo
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
    && pip install --no-cache-dir -r /mancelot/requirements.txt \
\
    # Because pygraphviz has to be installed with additional flags
    && pip install --install-option="--include-path=/usr/local/include/" \
        --install-option="--library-path=/usr/local/lib/" pygraphviz

# NB, we link the repo at runtime (which 'overwrites' files copied in on build)
# But production (when we run from image without linking the repo in) does use
# the files copied in!
COPY . /mancelot
COPY templates/flower/base.html /usr/local/lib/python3.7/site-packages/flower/templates/base.html
COPY tlrh/ /mancelot
RUN chown -R mancelot:mancelot /mancelot \
    && rm -rf tlrh

USER mancelot

ENTRYPOINT ["/mancelot/entrypoint.sh"]
