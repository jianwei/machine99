from utils.unix_socket import unix_socket
import json

import yaml

def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8')as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        return data

# u = unix_socket("../uds_socket")
unix_socket_path = get_yaml_data('../config.yaml').get('unix_socket')
u = unix_socket(unix_socket_path)
message = json.dumps({"a":1})
u.send_message(message)

