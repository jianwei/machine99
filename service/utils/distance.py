import time
import uuid,json
from utils.unix_socket_send import unix_socket_send
from utils.points import points
class distance():
    def __init__(self,cmd_server_address):
        self.cmd_server_address = cmd_server_address
        self.points = points()
        self.row_spacing = 90  #px

    

    def do(self,message):
        print("message:",message)
        ret = {}
        lines = self.points.split_line(message)
        ret["lines_format"] = lines
        ret["source"] = message
        return ret
        # print("lines:",lines)
        # self.get_px_diff(lines)
        # return "do message"
        # send_message = json.dumps({"uuid":str(uuid.uuid1()),"cmd":"distance","send_time":time.time()})
        # send_socket = unix_socket_send(self.cmd_server_address)
        # ret = send_socket.send_message(send_message)
    
    def get_px_diff(self,data):
        points = []
        for line in data:
            for item in line:
                points.append(float(item.get("centerx")))
        length = len(points)
        diff_points = []
        for i in range(length):
            item = points[i]
            print(item)
            if (i != (length-1)) : 
                diff_points.append(abs(points[i+1]-points[i]))
        print("get_px_diff:",diff_points)


    