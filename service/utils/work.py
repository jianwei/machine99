import time
import uuid,json
from utils.unix_socket_send import unix_socket_send
class work():
    def __init__(self,cmd_server_address):
        self.cmd_server_address = cmd_server_address
    
    def do(self,message):
        message = json.dumps({"uuid":str(uuid.uuid1()),"cmd":"LROT 255"})
        # print("work-do-message:",message)
        send_socket = unix_socket_send(self.cmd_server_address)
        ret = send_socket.send_message(message)