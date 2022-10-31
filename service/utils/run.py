from points import points
import time
import numpy
from serial_control import serial_control
import uuid
class run ():
    def __init__(self):
        self.points_obj = points()
        self.global_angle = 90
        self.angle_diff_px = 10  #像素10 以内不做调整
        self.max_angle = 10   #转向不超过 10度
        self.serial_control = serial_control()

    
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
        diff_point_x = center_pointer_x-target_turn_point_x
        tan = (diff_point_x)*unit/(gap+(screenSize[1]-target_turn_point_y)*unit)
        angle = numpy.arctan(tan) * 180.0 / 3.1415926
        print("angle:",angle)
        cmd_prefix = "TR" if target_turn_point_x<center_pointer_x else "TL"
        if (int(abs(angle))<=10 and int(abs(angle))>=3):
            cmd = "{} {}".format(cmd_prefix,int(angle))
            self.global_angle += angle
            # self.serial_control.send_cmd({"uuid":str(uuid.uuid1()),"cmd":cmd})
