import os,yaml
import threading

def main():
    config = get_yaml_data("../config.yaml")
    cameras = config.get("camera")
    for item in cameras:
        cmd = "python3 detect.py --camera_id {} --to_do {}".format(item.get("camera_id"),item.get("to_do"))
        thread = threading.Thread(target=run_cmd, args=(cmd,))
        thread.start()

def run_cmd(cmd):
    print("cmd:",cmd)
    os.system(cmd)

def get_yaml_data(config_yaml):
    with open(config_yaml, encoding='utf-8') as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        return data

if __name__ == '__main__':
    main()
    # cmds = ["python3 detect.py --camera_id 0 --to_do work","python3 detect.py --camera_id 2 --to_do run"]
    # cmd_arr = [
    #     {
    #         "camera_id":"0",
    #         "to_do":"run1",
    #     },{
    #         "camera_id":"2",
    #         "to_do":"run2",
    #     },{
    #         "camera_id":"4",
    #         "to_do":"work",
    #     }
    # ]
    # cmds = []
    # for item in cmd_arr:
    #     cmd = "python3 detect.py --camera_id {} --to_do {}".format(item.get("camera_id"),item.get("to_do"))
    #     cmds.append(cmd)
    # # cmds = ["python3 detect.py --camera_id 0 --to_do work","python3 detect.py --camera_id 2 --to_do run"]
    # main(cmds)