import json
from utils.serial_control import serial_control

class deal_message():
    def __init__(self):
        self.serial_control = serial_control()


    def do_message(self, message):
        if (message):
            message = json.loads(message)
            # message  {"uuid":str(uuid.uuid1()),"cmd":cmd}
            self.serial_control.send_cmd(message)


