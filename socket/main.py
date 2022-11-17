from utils.unix_socket import unix_socket
import yaml

def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8') as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        print("get_yaml_data:",data)
        return data

def main():
    unix_socket_path = get_yaml_data('../config.yaml').get('serial_control').get("unix_socket")
    print("unix_socket_path:{}".format(unix_socket_path))
    u = unix_socket(unix_socket_path)
    u.server()


if __name__ == '__main__':
    main()