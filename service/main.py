from utils.unix_socket_server import unix_socket_server
import yaml,argparse

def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8') as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        # print("get_yaml_data:",data)
        return data

def main(to_do='near'):
    yaml_config = get_yaml_data('../config.yaml')
    camera_unix_socket_path = get_unix_socket(yaml_config.get("camera"),to_do)
    cmd_unix_socket_path = yaml_config.get("serial_control").get("unix_socket")
    print("camera_unix_socket_path:{},cmd_unix_socket_path:{}".format(camera_unix_socket_path,cmd_unix_socket_path))
    u = unix_socket_server(camera_unix_socket_path,cmd_unix_socket_path,to_do)
    u.server()


def get_unix_socket(cameras,to_do):
    for item in cameras:
        if(to_do==item.get("to_do")):
            return item.get("unix_socket")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--to_do', type=str,default="near", help='run or work')
    opt = parser.parse_args()
    # print(opt,type(opt))
    main(**vars(opt))