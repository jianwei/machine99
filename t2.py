import os,sys
import socket

server_address = './uds_socket'
server_address2 = './uds_socket2'
 
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(server_address)

server.listen(1)

sock2 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    sock2.connect(server_address2)
except socket.error as msg:
    print(msg)
    sys.exit(1)

# for i in range(100):
#     message = "hello world,t1 send:{}".format(i)
#     print(message)
#     sock2.send(message.encode("UTF-8"))
#     time.sleep(1)
# sock.close()


while True:
    connection, client_address = server.accept()
    try:
        data_str = ""
        while True:
            data = connection.recv(102400)
            data_str += data.decode()
            if data:
                print(data)
                # message = "hello world,t1 send:"
                sock2.send(data)
            else:
                break
    finally:
        # Clean up the connection
        connection.close()



