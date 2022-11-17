# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid


class unix_socket_send():
    def __init__(self,server_address):
        self.server_address = server_address
        self.send_cmd_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self.send_cmd_socket.connect(self.server_address)
        except socket.error as msg:
            print("send_message,error:",msg)
            sys.exit(1)

    def send_message(self,message):
        print('connecting to {}'.format(self.server_address))
        try:
            message = message.encode('utf-8')
            print('sending {!r}'.format(message))
            self.send_cmd_socket.sendall(message)

            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.send_cmd_socket.recv(1024)
                amount_received += len(data)
                # print('received {!r}'.format(data))
                return data.decode('utf-8')

        finally:
            print('finally socket')
            # self.socket.close()