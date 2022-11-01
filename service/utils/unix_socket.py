# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid
from utils.deal_message import deal_message


class unix_socket():
    def __init__(self,server_address,to_do='run'):
        # print("server_address:",server_address)
        self.server_address = server_address
        self.to_do = to_do
        self.deal_message = deal_message()
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
            print('waiting for a connection')
            connection, client_address = self.socket.accept()
            try:
                data_str = ""
                while True:
                    data = connection.recv(102400)
                    data_str += data.decode()
                    if data:
                        reasult = self.deal_message.do_message(str(data.decode()),self.to_do)
                        if (type(reasult)==str):
                            reasult = reasult.encode('UTF-8')
                        # print('data:{},reasult:{}'.format(data,reasult))
                        print('reasult:{}'.format(reasult))
                        connection.sendall(reasult)
                    else:
                        break
            finally:
                # Clean up the connection
                connection.close()
    
    
                
        

