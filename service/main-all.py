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
    cmds = ["python3 main.py --to_do run","python3 main.py --to_do work"]
    main(cmds)