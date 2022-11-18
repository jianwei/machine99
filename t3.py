import os
import socket

server_address = './uds_socket2'
 
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(server_address)

server.listen(1)

while True:
    connection, client_address = server.accept()
    try:
        data_str = ""
        while True:
            data = connection.recv(102400)
            data_str += data.decode()
            if data:
                print(data)
            else:
                break
    finally:
        # Clean up the connection
        connection.close()