from utils.unix_socket import unix_socket
import yaml

def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8')as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        return data

unix_socket_path = get_yaml_data('../config.yaml').get('unix_socket')
u = unix_socket(unix_socket_path)
u.server()
