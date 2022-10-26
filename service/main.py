from utils.unix_socket import unix_socket


u = unix_socket("../uds_socket")
u.server()
