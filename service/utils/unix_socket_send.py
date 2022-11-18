# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid


class unix_socket_send():
    def __init__(self,server_address):
        self.server_address = server_address
       

    def send_message(self,message):
        # print('connecting to {}'.format(self.server_address))
        try:
            message = message if isinstance(message,bytes) else message.encode('utf-8')
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                sock.connect(self.server_address)
            except socket.error as msg:
                print("sock.connect error:",msg)
                sys.exit(1)
            sock.send(message)
            sock.close()

        finally:
            print('finally socket')
            # self.socket.close()