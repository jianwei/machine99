# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid
sys.path.append("..")
from service.utils.deal_message import deal_message


class unix_socket():
    def __init__(self,is_server=False):
        self.server_address = './uds_socket'
        if(is_server):
            try:
                os.unlink(self.server_address)
            except OSError:
                if os.path.exists(self.server_address):
                    raise
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        

    def server(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        done = deal_message()
        while True:
            print('waiting for a connection')
            connection, client_address = self.socket.accept()
            try:
                data_str = ""
                while True:
                    data = connection.recv(10)
                    data_str += data.decode()
                    print('data-----------:',data_str)
                    if data:
                        print('sending data back to the client',data)
                        connection.sendall(data)
                    else:
                        print('no data from:{},data:{}'.format(client_address,data_str))
                        deal_message.do_message(data_str)
                        break
            finally:
                # Clean up the connection
                connection.close()
    
    def send_message(self,message):
        print('connecting to {}'.format(self.server_address))
        try:
            self.socket.connect(self.server_address)
        except socket.error as msg:
            print("send_message,error:",msg)
            sys.exit(1)
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
            print('closing socket')
            self.socket.close()
                
        

