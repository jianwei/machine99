import os,sys
import socket,time

server_address = './uds_socket'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    sock.connect(server_address)
except socket.error as msg:
    print(msg)
    sys.exit(1)

for i in range(100):
    message = "hello world,t1 send:{}".format(i)
    print(message)
    sock.send(message.encode("UTF-8"))
    time.sleep(1)
sock.close()