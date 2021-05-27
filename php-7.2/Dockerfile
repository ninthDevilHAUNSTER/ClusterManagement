FROM webdevops/php-nginx:7.2
RUN pecl install xdebug && \
        docker-php-ext-enable xdebug
RUN apt-get update && apt-get install -y mlocate \
                                     libfreetype6-dev \
                                     libjpeg62-turbo-dev \
                                     libwebp-dev \ 
                                     libxpm-dev \
                                     libpng-dev && \
docker-php-ext-configure gd --with-freetype-dir --with-jpeg-dir --with-png-dir --with-webp-dir --with-xpm-dir && \
docker-php-ext-install -j$(nproc) gd

RUN chmod -R 777 /app/
RUN chown -R application:application /app/

RUN echo "xdebug.remote_enable = 1" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
RUN echo "xdebug.mode=coverage" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
RUN echo "auto_prepend_file = \"/var/www/xdebug_script/prepend_xdebug_offline.php\"" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
