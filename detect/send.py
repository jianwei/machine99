from utils.unix_socket import unix_socket
import json

u = unix_socket("../uds_socket")
message = json.dumps({"a":1})
u.send_message(message)

