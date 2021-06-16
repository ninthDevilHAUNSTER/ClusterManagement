FROM webdevops/php-nginx:7.4

RUN pecl install xdebug-2.9.0 && \
        docker-php-ext-enable xdebug
        
RUN sed -i "s/http:\/\/deb.debian.org/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
	sed -i "s/http:\/\/security.debian.org/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list 

RUN apt-get update && \ 
	apt-get install -y mlocate libfreetype6-dev libjpeg62-turbo-dev libwebp-dev libxpm-dev libpng-dev && \ 
    docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp && \
	docker-php-ext-install -j$(nproc) gd && \
    apt-get -y autoremove && \ 
    rm -rf /var/lib/apt/lists/*  

RUN chmod -R 777 /app/ && \
	chown -R application:application /app/

COPY files/xdebug-2.9.0 /xdebug

RUN cd /xdebug && phpize && ./configure && make && make install

RUN echo "xdebug.remote_enable = 1" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
	echo "xdebug.mode=coverage" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
	echo "auto_prepend_file = \"/var/www/xdebug_script/prepend_xdebug_offline.php\"" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini