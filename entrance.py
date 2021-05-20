#! /usr/bin/python3.9

# @Time : 2021/5/16 14:40
# @Author : ShaoBaoBaoEr
# @Site : 
# @File : create_docker.py
# @Software: PyCharm

import argparse
import os

STR_B = """
version: '2'

services:
  php-apache:
    build: .
    ports:
      - {port}:80
    volumes:
      - ./www/:/app/
      - ../xdebug_script/:/var/www/xdebug_script/
    restart: always
    networks:
      - appg_network_group

networks:
  appg_network_group:
    external:
      name: appg_network_group
"""

__description = "ClusterManagement , Easy to automatic trace various php application via docker"
parser = argparse.ArgumentParser(prog="ClusterManagement", description=__description)
parser.add_argument("--php", dest="php_version", action="store", type=str, default="5.6",
                    metavar="php_version", help="PHP版本")
parser.add_argument("-z", "--zip", dest="zip_file", action="store", type=str, metavar="zip_file",
                    help="源代码压缩文件（ZIP）")  # ./source_code_ftp/
parser.add_argument("-p", "--port", dest="port", action="store", type=int, metavar="port")
parser.add_argument("-a", "--action", dest="action", action="store", type=str, required=True, metavar="action",
                    help="extract : 提取源码\nconnect : 连接容器 \n build : 构建容器 \n build_docker : 构建并启动容器")
parser.add_argument("-d", "--data", dest="data", action="store", type=str, metavar="data")
ENTRANCE_PARAMS = parser.parse_args()


def docker_container_name_filter_20_10_2(dir_name):
    """
    container name filter on
        Docker version 20.10.2, build 20.10.2-0ubuntu1~18.04.2
    :return:
    """
    return dir_name.rstrip("/").lstrip("./").replace("_", "").replace(".", "").replace("-", "").lower()


if ENTRANCE_PARAMS.action in ['build_docker', 'build']:
    assert ENTRANCE_PARAMS.port is not None
    assert ENTRANCE_PARAMS.zip_file is not None
    assert os.path.exists(ENTRANCE_PARAMS.zip_file)
    assert ENTRANCE_PARAMS.php_version in ['5.6', '7.4', '7.2']
    base_name = os.path.basename(os.path.realpath(ENTRANCE_PARAMS.zip_file))
    tag_name = base_name.rstrip(".zip")
    os.system(f"unzip -q {ENTRANCE_PARAMS.zip_file}  -d ./tmp")
    os.system(f"cp -r php-{ENTRANCE_PARAMS.php_version} {tag_name}")
    os.system(f"mv ./tmp/{tag_name}/* ./{tag_name}/www/")
    os.system(f"chmod -R 777 ./{tag_name}/www/")
    open(f"./{tag_name}/docker-compose.yml", 'w').write(
        STR_B.format(port=ENTRANCE_PARAMS.port)
    )
    os.system(f"rm -rf ./tmp/")
    os.system(f"docker-compose -f ./{tag_name}/docker-compose.yml up --build -d")

elif ENTRANCE_PARAMS.action in ['up']:
    assert ENTRANCE_PARAMS.data is not None
    os.system(f"docker-compose -f ./{ENTRANCE_PARAMS.data}/docker-compose.yml up --build -d")


elif ENTRANCE_PARAMS.action in ['extract', "extract_build_code"]:
    assert ENTRANCE_PARAMS.data is not None
    os.system(f"zip -q -r ./source_code_build_ftp/{ENTRANCE_PARAMS.data}.zip ./{ENTRANCE_PARAMS.data}/www/ ")

elif ENTRANCE_PARAMS.action in ['connect', 'ssh']:
    assert ENTRANCE_PARAMS.data is not None
    ENTRANCE_PARAMS.data = ENTRANCE_PARAMS.data.rstrip("/")
    ENTRANCE_PARAMS.data = docker_container_name_filter_20_10_2(ENTRANCE_PARAMS.data)

    if ENTRANCE_PARAMS.data == "codecoverage":
        os.system(
            f"docker exec -it {ENTRANCE_PARAMS.data}_db_1 /usr/bin/mysql -uroot -ppassword")
    else:
        os.system(
            f"docker exec -it {ENTRANCE_PARAMS.data}_php-apache_1 /bin/bash")

elif ENTRANCE_PARAMS.action in ['delete']:
    assert ENTRANCE_PARAMS.data is not None
    assert os.path.exists(ENTRANCE_PARAMS.data)
    os.system(f"docker-compose -f ./{ENTRANCE_PARAMS.data}/docker-compose.yml down")
    os.system(f"rm -rf ./{ENTRANCE_PARAMS.data}")
