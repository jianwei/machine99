import os
import threading
import yaml


def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8') as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        return data

def main():
    yaml_config = get_yaml_data('../config.yaml')
    cameras = yaml_config.get("camera")
    for item in cameras:
        cmd = "python3 main.py --to_do {}".format(item.get("to_do"))
        print(cmd)
        thread = threading.Thread(target=run_cmd, args=(cmd,))
        thread.start()

def run_cmd(cmd):
    print("cmd:",cmd)
    os.system(cmd)

if __name__ == '__main__':
    # cmds = ["python3 main.py --to_do run1","python3 main.py --to_do run2","python3 main.py --to_do work"]
    main()