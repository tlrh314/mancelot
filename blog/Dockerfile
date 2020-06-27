FROM php:7.4-fpm

WORKDIR /blog

RUN set -ex \
  && apt-get update && apt-get install -y \
  # WordPress requirements
  libmagickwand-dev zlib1g-dev libzip-dev --no-install-recommends \
  \ 
  && docker-php-ext-install mysqli && docker-php-ext-enable mysqli \
  && docker-php-ext-install exif zip gd \
  \
  && pecl install imagick \ 
  && docker-php-ext-enable imagick \
  \
  # Clear cache
  && apt-get clean && rm -rf /var/lib/apt/lists/* \
  \
  # Add user to run the php application
  && groupadd -g 1000 mancelot \
  && useradd -u 1000 -ms /bin/bash -g mancelot mancelot

# Copy application directory contents
COPY . /blog

# Copy application directory permissions
COPY --chown=mancelot:mancelot . /blog

USER mancelot

EXPOSE 9000
CMD ["php-fpm"]
