# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid
from utils.deal_message import deal_message


class unix_socket():
    def __init__(self,server_address,cmd_server_address,to_do='run'):
        # print("server_address:",server_address)
        self.server_address = server_address
        self.cmd_server_address = cmd_server_address
        self.to_do = to_do
        self.deal_message = deal_message()
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.send_cmd_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self.send_cmd_socket.connect(self.cmd_server_address)
        except socket.error as msg:
            print("send_message,error:",msg)
            sys.exit(1)

    def send_message(self,message):
        # print('connecting to {}'.format(self.server_address))
        try:
            message = message.encode('utf-8')
            # print('sending {!r}'.format(message))
            self.send_cmd_socket.sendall(message)

            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.socket.recv(102400)
                amount_received += len(data)
                # print('received {!r}'.format(data))
                return data.decode('utf-8')

        finally:
            print('finally socket')
            # self.socket.close()
        

    def server(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        while True:
            print('waiting for {} connection:,send_cmd_socket:{}{}'.format(self.to_do,self.send_cmd_socket,type(self.send_cmd_socket)))
            connection, client_address = self.socket.accept()
            try:
                data_str = ""
                while True:
                    data = connection.recv(102400)
                    data_str += data.decode()
                    if data:
                        reasult = self.deal_message.do_message(str(data.decode()),self.to_do,self.send_cmd_socket)
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
    
    
                
        

