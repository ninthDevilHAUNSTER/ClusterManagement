# Cluster Management

## What is it?

A cluster build via docker.

Easy to automatic trace various php application via docker

## How to use it?

```shell
git clone ...
chmod -R 777 xdebug_script

cd code_coverage
docker-compose up --build -d
cd ..

cd common-php-7.4-xdebug
docker-compose up --build -d
```

**Default database setup**

on localhost:21306 , here is a database used for code coverage

otherwise ,via modify prepend_xdebug_offline.php.bak , it can be switched to file storage mode
