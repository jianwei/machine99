
from utils.unix_socket_send import unix_socket_send
import uuid,json,time

class turn_around():
    
    def __init__(self,cmd_server_address):
        # self.long = 100 #cm
        self.cmd_server_address  = cmd_server_address
        self.first_round_time = 1 #s 第一次原地旋转时间
        self.second_round_time = 1 #s 第二次原地旋转时间
        self.first_go_time = 1 #s 原地旋转结束后，向前行驶时间
        self.turn_speed = 100
        unit_sleep = 1/(self.turn_speed*50/2/1000)   #转1圈所需要的时间
        self.turn_time = unit_sleep/4

    def turn_left(self):
        self.first_round_time = 3 #s 原地旋转时间
        self.second_round_time = 3 #s 原地旋转时间


    
    def turn_cmd(self,cmd):
        send_socket = unix_socket_send(self.cmd_server_address)
        message = json.dumps({"uuid":str(uuid.uuid1()),"cmd":cmd,"send_time":time.time()})
        ret = send_socket.send_message(message)
        return ret


    def set_turn_status(self):
        t0 = time.time()
           #左前轮 右转45度
        cmd = "LFTR {}.".format(self.turn_speed)
        self.turn_cmd(cmd)
            #右前轮 左转45度
        cmd = "RFTL {}.".format(self.turn_speed)
        self.turn_cmd(cmd)
            #左后轮 右转45度
        cmd = "LRTR {}.".format(self.turn_speed)
        self.turn_cmd(cmd)
            #右后轮 左转45度
        cmd = "RRTL {}.".format(self.turn_speed)
        self.turn_cmd(cmd)
        t1 = time.time()
        diff = t1-t0
        if(diff<self.turn_time):
            time.sleep(self.turn_time-diff)
        self.turn_cmd("STOP 3.")
    
    def back_turn_status(self):
        t0 = time.time()
           #左前轮 左转45度
        cmd = "LFTL {}.".format(self.turn_speed)
        self.turn_cmd(cmd)
            #右前轮 右转45度
        cmd = "RFTR {}.".format(self.turn_speed)
        self.turn_cmd(cmd)
            #左后轮 左转45度
        cmd = "LRTL {}.".format(self.turn_speed)
        self.turn_cmd(cmd)
            #右后轮 右转45度
        cmd = "RRTR {}.".format(self.turn_speed)
        self.turn_cmd(cmd) 
        t1 = time.time()
        diff = t1-t0
        if(diff<self.turn_time):
            time.sleep(self.turn_time-diff)
        self.turn_cmd("STOP 3.")


    def _turn_round(self):
        #旋转角度
        self.set_turn_status() 
        #旋转
        self.turn_cmd("MF 30.")
        time.sleep(self.first_round_time)
        self.turn_cmd("STOP 1.")
        #复位角度
        self.back_turn_status()
        #前进
        self.turn_cmd("MF 30.")
        time.sleep(self.first_go_time)
        self.turn_cmd("STOP 1.")
        #旋转角度
        self.set_turn_status()
        #旋转
        self.turn_cmd("MF 30.")
        time.sleep(self.second_round_time)
        self.turn_cmd("STOP 1.") 
        #复位角度
        self.back_turn_status()