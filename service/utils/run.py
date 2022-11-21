from utils.points import points
import time
import numpy
# from utils.serial_control import serial_control
from utils.unix_socket_send import unix_socket_send
import uuid
import json
class run ():
    def __init__(self,cmd_server_address):
        self.points_obj = points()
        self.global_angle = 90
        self.angle_diff_px = 10  #像素10 以内不做调整
        self.max_angle = 10   #转向不超过 10度
        # self.serial_control = serial_control()
        self.cmd_server_address  = cmd_server_address
        self.last_turn_time = 0
        

    
    def do(self,message):
        target_turn_point_x = self.points_obj.get_turn_point_x(message)
        target_turn_point_y = self.points_obj.get_turn_point_y(message)
        print("target_turn_point:",target_turn_point_x,target_turn_point_y)
        self.turn(message,target_turn_point_x,target_turn_point_x)


    def turn(self,data,target_turn_point_x,target_turn_point_y):
        unit = 0.0386  # 1 pint 0.0386cm
        gap = 30  # cm 导航摄像头的视野盲区
        screenSize = data[0].get("screenSize")
        center_pointer_x = screenSize[0]/2  # 640px中间
        is_turn_left = False if center_pointer_x>target_turn_point_x else True
        diff_point_x = abs(center_pointer_x-target_turn_point_x) 
        tan = diff_point_x/(screenSize[1]-target_turn_point_y)
        tan = (diff_point_x)*unit/(gap+(screenSize[1]-target_turn_point_y)*unit)
        angle = numpy.arctan(tan) * 180.0 / 3.1415926
        cmd_prefix = "TR" if is_turn_left else "TL"
        print("center_pointer_x:{},target_turn_point_x:{},is_turn_left:{}".format(center_pointer_x,target_turn_point_x,is_turn_left))


        # if (int(abs(angle))<=10 and int(abs(angle))>=3):
        cmd = "{} {}".format(cmd_prefix,int(angle))
        # cmd = "{} {}.".format(cmd_prefix,10)
        self.global_angle += angle
        message = json.dumps({"uuid":str(uuid.uuid1()),"cmd":cmd,"send_time":time.time()})
        # print("send cmd message:",message)
        # self.serial_control.send_cmd(message)
        # self.unix_socket_send(message)
        send_socket = unix_socket_send(self.cmd_server_address)
        ret = send_socket.send_message(message)
        print("send cmd message ret--------------------------------------------------+++++++++++++++++:",ret)
