# -*- coding:utf-8 -*-
import os
import socket
import json
from utils.serial_control import serial_control


class unix_socket():
    def __init__(self,server_address):
        self.server_address = server_address
        self.serial_control = serial_control()
        print("self.server_address:",self.server_address)
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
        

    def server(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        while True:
            print('waiting for cmd socket connection')
            connection, client_address = self.socket.accept()
            try:
                data_str = ""
                while True:
                    data = connection.recv(102400)
                    data_str += data.decode()
                    if data:
                        message = str(data.decode())
                        if (message):
                            message = json.loads(message)
                            # message  {"uuid":str(uuid.uuid1()),"cmd":cmd}
                            self.serial_control.send_cmd(message)
                        if (type(reasult)==str):
                            reasult = reasult.encode('UTF-8')
                        print('reasult:{}'.format(reasult))
                        connection.sendall(reasult)
                    else:
                        break
            finally:
                # Clean up the connection
                connection.close()
    
    
                
        

