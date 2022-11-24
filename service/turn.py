import time,os
from utils.turn_around import turn_around
from utils.redis_connect import redis_connect
import yaml,argparse

def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8') as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        return data

def main():
    yaml_config = get_yaml_data('../config.yaml')
    cmd_server_address = yaml_config.get("camera").get("serial_control").get("unix_socket")
    redis = redis_connect()
    turn_obj = turn_around(cmd_server_address)
    while (True):
        time.sleep(1)
        need_turn = redis.get("need_turn")
        if(int(need_turn)==1):
            turn_obj._turn_round()
            redis.set("need_turn",0)

if __name__ == '__main__':
    main()
    