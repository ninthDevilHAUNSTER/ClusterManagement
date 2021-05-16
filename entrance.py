# @Time : 2021/5/16 14:40
# @Author : ShaoBaoBaoEr
# @Site : 
# @File : create_docker.py
# @Software: PyCharm

import argparse
import os

__description = "ClusterManagement , Easy to automatic trace various php application via docker"
parser = argparse.ArgumentParser(prog="ClusterManagement", description=__description)
parser.add_argument("--php", dest="php_version", action="store", type=str, default="5.6",
                    metavar="php_version", help="PHP版本")
parser.add_argument("-z", "--zip", dest="zip_file", action="store", type=str, metavar="zip_file",
                    help="源代码压缩文件（ZIP）")  # ./source_code_ftp/
parser.add_argument("-p", "--port", dest="port", action="store", type=int, metavar="port")
parser.add_argument("-a", "--action", dest="action", action="store", type=str, required=True, metavar="action")
parser.add_argument("-d", "--data", dest="data", action="store", type=str, metavar="data")
ENTRANCE_PARAMS = parser.parse_args()

if ENTRANCE_PARAMS.action in ['build_docker', 'build']:
    assert ENTRANCE_PARAMS.port is not None
    assert ENTRANCE_PARAMS.zip_file is not None
    assert os.path.exists(ENTRANCE_PARAMS.zip_file)
    assert ENTRANCE_PARAMS.php_version in ['5.6', '7.4']
    base_name = os.path.basename(os.path.realpath(ENTRANCE_PARAMS.zip_file))
    tag_name = base_name.rstrip(".zip")
    os.system(f"unzip {ENTRANCE_PARAMS.zip_file} -d ./tmp")
    os.system(f"cp -r common-php-{ENTRANCE_PARAMS.php_version}-xdebug {tag_name}")
    os.system(f"mv ./tmp/{tag_name}/* ./{tag_name}/www/")
    os.system(f"chmod -R 777 ./{tag_name}/www/")
    os.system(
        f"sed 's/30000/{ENTRANCE_PARAMS.port}/' ./{tag_name}/docker-compose.yml > ./{tag_name}/docker-compose.yml")
    os.system(f"rm -rf ./tmp")
elif ENTRANCE_PARAMS.action in ['extract', "extract_build_code"]:
    assert ENTRANCE_PARAMS.data is not None
    os.system(f"zip -q -r ./source_code_build_ftp/{ENTRANCE_PARAMS.data}.zip ./{ENTRANCE_PARAMS.data}/www/ ")
