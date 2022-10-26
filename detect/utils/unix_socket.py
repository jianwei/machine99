# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid


class unix_socket():
    def __init__(self,server_address):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.server_address)
        except socket.error as msg:
            print("send_message,error:",msg)
            sys.exit(1)
        
    
    def send_message(self,message):
        print('connecting to {}'.format(self.server_address))
        try:
            message = message.encode('utf-8')
            print('sending {!r}'.format(message))
            self.socket.sendall(message)

            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.socket.recv(1024)
                amount_received += len(data)
                print('received {!r}'.format(data))
                return data.decode('utf-8')

        finally:
            print('finally socket')
            # self.socket.close()
                
        

