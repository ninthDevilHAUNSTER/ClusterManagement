# Cluster Management

## What is it?

A cluster build via docker.

Easy to automatic trace various php application via docker

## How to use it?

Use raw docker-compose command
```shell
git clone ...
chmod -R 777 xdebug_script

cd code_coverage
docker-compose up --build -d
cd ..

cd common-php-7.4-xdebug
docker-compose up --build -d
```

Use entrance.py command

```shell
λ python entrance.py  --help
usage: ClusterManagement [-h] [--php php_version] [-z zip_file] [-p port] -a
                         action [-d data]

ClusterManagement , Easy to automatic trace various php application via docker

optional arguments:
  -h, --help            show this help message and exit
  --php php_version     PHP版本
  -z zip_file, --zip zip_file
                        源代码压缩文件（ZIP）
  -p port, --port port
  -a action, --action action
                        extract : 提取源码 connect : 连接容器 build : 构建容器
                        build_docker : 构建并启动容器
  -d data, --data data
```

## Setup

```shell
# build database for strorage
cd code_coverage
docker-compose up --build -d
# build docker 
python entrance.py  -a build -z ./source_code_ftp/Wordpress-5.1.zip --port 30000 --php 7.2 
# connect docker
python entrance.py -a ssh -d Wordpress-5.1 

```
