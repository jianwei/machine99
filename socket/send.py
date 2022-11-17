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


# u = unix_socket("../uds_socket")
server_address = get_yaml_data('../config.yaml').get("serial_control").get('unix_socket')


# server_address = './uds_socket'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    sock.connect(server_address)
except socket.error as msg:
    print(msg)
    sys.exit(1)

# message = json.dumps({"uuid": })
# sock.send(b'{"": 1}')
# sock.close()
# u = unix_socket(unix_socket_path)
for i in range(100):
    message = json.dumps({"uuid": i,"cmd":"TR {}".format(i+10)})
    # u.send_message(message)
    sock.send(message)
    time.sleep(1)
