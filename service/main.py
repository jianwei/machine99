from utils.unix_socket import unix_socket
import yaml,argparse

def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8') as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        print("get_yaml_data:",data)
        return data

def main(to_do='run'):
    unix_socket_path = get_yaml_data('../config.yaml').get('unix_socket').get(to_do)
    print("to_do:",to_do)
    u = unix_socket(unix_socket_path,to_do)
    u.server()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--to_do', type=str,default="run", help='run or work')
    opt = parser.parse_args()
    # print(opt,type(opt))
    main(**vars(opt))