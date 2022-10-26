# -*- coding:utf-8 -*-
import os
import socket
import sys
import time,uuid



class unix_socket():
    def __init__(self,server_address):
        self.server_address = server_address
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        

    def server(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        # done = deal_message()
        while True:
            print('waiting for a connection')
            connection, client_address = self.socket.accept()
            try:
                data_str = ""
                while True:
                    data = connection.recv(1024)
                    data_str += data.decode()
                    if data:
                        print('sending data back to the client',data)
                        connection.sendall(data)
                    else:
                        break
            finally:
                # Clean up the connection
                connection.close()
    
    
                
        

