import os
import threading

def main(cmds):
    for cmd in cmds:
        thread = threading.Thread(target=run_cmd, args=(cmd,))
        thread.start()


def run_cmd(cmd):
    print("cmd:",cmd)
    os.system(cmd)

if __name__ == '__main__':
    cmds = ["python3 detect.py --camera_id 20 --to_do run","python3 detect.py --camera_id 22 --to_do work"]
    main(cmds)