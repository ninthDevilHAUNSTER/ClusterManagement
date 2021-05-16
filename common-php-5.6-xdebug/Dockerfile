FROM ghcr.io/mileschou/xdebug:5.6-apache 

ENV COMPOSER_PATH /usr/local/bin/composer

# Install extensions
RUN set -xe && \
        apt-get update -y && apt-get install -y --no-install-recommends --no-install-suggests \
            libgmp-dev \
            libjpeg-dev \
            libmemcached-dev \
            libpng-dev \
            libxml2-dev \
            libzip-dev \
            zlib1g-dev
RUN ln -s /usr/include/x86_64-linux-gnu/gmp.h /usr/include/gmp.h

RUN apt-get clean && rm -rf /var/lib/apt/lists/* \
        && \
        # See https://github.com/docker-library/php/issues/912#issuecomment-559918036
        docker-php-ext-configure gd \
            --with-jpeg \
        && \
        docker-php-ext-install -j $(getconf _NPROCESSORS_ONLN) \
            bcmath \
            exif \
            gd \
            gmp \
            pdo_mysql \
            mysqli \
            soap \
            sockets \
            zip 

RUN php -m
# Install Composer v2
COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

# Modify Xdebug
#RUN mkdir /var/www/xdebug_script
#RUN mkdir /var/www/xdebug_script/coverage
#RUN chmod -R 777 /var/www/xdebug_script/

RUN echo "xdebug.remote_enable = 1" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
RUN echo "xdebug.mode=coverage" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
RUN echo "auto_prepend_file = \"/var/www/xdebug_script/prepend_xdebug_offline.php\"" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
