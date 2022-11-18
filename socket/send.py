from utils.unix_socket import unix_socket
import json
import yaml
import time
import os
import socket,sys


def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8')as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        return data


server_address = get_yaml_data('../config.yaml').get("serial_control").get('unix_socket')
# sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# try:
#     sock.connect(server_address)
# except socket.error as msg:
#     print(msg)
#     sys.exit(1)


for i in range(30):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(server_address)
    except socket.error as msg:
        print(msg)
    message = json.dumps({"uuid": i,"cmd":"TR {}".format(i+10)})
    print(message)
    sock.send(message.encode("UTF-8"))
    sock.close()
    time.sleep(1)
