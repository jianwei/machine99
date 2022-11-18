# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid


class unix_socket_send():
    def __init__(self,server_address):
        self.server_address = server_address
        # self.send_cmd_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # try:
        #     self.send_cmd_socket.connect(self.server_address)
        # except socket.error as msg:
        #     print("send_message,error:",msg)
        #     sys.exit(1)

    def send_message(self,message):
        print('connecting to {}'.format(self.server_address))
        try:
            # message = message.encode('utf-8')
            # sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            # try:
            #     sock.connect(self.server_address)
            # except socket.error as msg:
            #     print("sock.connect error:",msg)
            #     sys.exit(1)
            # sock.send(message)
            # sock.close()


            send_cmd_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                send_cmd_socket.connect(self.server_address)
            except socket.error as msg:
                print("send_message,error:",msg)
                sys.exit(1)

            print('sending {!r}'.format(message))
            send_cmd_socket.sendall(message)

            amount_received = 0
            amount_expected = len(message)
            j = 1
            while amount_received < amount_expected:
                j+=1
                print("j============",j)
                data = send_cmd_socket.recv(102400)
                amount_received += len(data)
                print('received {!r}'.format(data))
                return data.decode('utf-8')

        finally:
            print('finally socket')
            # self.socket.close()