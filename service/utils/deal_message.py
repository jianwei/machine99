import json
import threading
from utils.run import run 
from utils.work import work 



class deal_message():

    def __init__(self):
        self.run_thread = ""
        self.work_thread = ""
        self.run_obj = run()
        self.work_obj = work()


    def do_message(self, message,to_do,send_cmd_socket):
        ret = {"message":"done"}
        if (message):
            # print("message:",message,type(message))
            message = json.loads(message)
            if (to_do=="near"):
                if (self.run_thread!="" and self.run_thread.is_alive()):
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++near")
                    ret["message"] = "near_thread is_alive"
                else:
                    print("----------------------------------------------------------------------------------------near")
                    self.run_thread = threading.Thread(target=self.run_obj.do, args=(message,send_cmd_socket,))
                    self.run_thread.start()
                    ret["message"] = "near_thread done"
            elif (to_do=="work" ):
                if (self.work_thread!="" and self.work_thread.is_alive()):
                    ret["message"] = "work_thread is_alive"
                else:
                    self.work_thread = threading.Thread(target=self.work_obj.do, args=(message,))
                    self.work_thread.start()
                    ret["message"] = "work_thread done"
        else:
            ret["message"] = "message is none,message:{}".format(message)
        return json.dumps(ret)



if __name__ == '__main__':
    points = [{"point": [[103, 166], [192, 166], [103, 238], [192, 238]], "name": "box", "time": 1666934463.3049679, "center": [147.5, 202.0], "centerx": 147.5, "centery": 202.0, "screenSize": [640, 480]}, {"point": [[18, 329], [135, 329], [18, 420], [135, 420]], "name": "box", "time": 1666934463.3058758, "center": [76.5, 374.5], "centerx": 76.5, "centery": 374.5, "screenSize": [640, 480]}, {"point": [[242, 77], [309, 77], [242, 118], [309, 118]], "name": "box", "time": 1666934463.3065524, "center": [275.5, 97.5], "centerx": 275.5, "centery": 97.5, "screenSize": [640, 480]}, {"point": [[261, 167], [339, 167], [261, 230], [339, 230]], "name": "box", "time": 1666934463.3071542, "center": [300.0, 198.5], "centerx": 300.0, "centery": 198.5, "screenSize": [640, 480]}, {"point": [[420, 160], [499, 160], [420, 217], [499, 217]], "name": "box", "time": 1666934463.3079154, "center": [459.5, 188.5], "centerx": 459.5, "centery": 188.5, "screenSize": [640, 480]}, {"point": [[482, 325], [608, 325], [482, 415], [608, 415]], "name": "box", "time": 1666934463.3086474, "center": [545.0, 370.0], "centerx": 545.0, "centery": 370.0, "screenSize": [640, 480]}, {"point": [[265, 336], [365, 336], [265, 427], [365, 427]], "name": "box", "time": 1666934463.3094497, "center": [315.0, 381.5], "centerx": 315.0, "centery": 381.5, "screenSize": [640, 480]}, {"point": [[152, 85], [212, 85], [152, 118], [212, 118]], "name": "box", "time": 1666934463.3102264, "center": [182.0, 101.5], "centerx": 182.0, "centery": 101.5, "screenSize": [640, 480]}]
    # points_center = [{"point": [[417, 163], [232, 163], [417, 508], [232, 508]], "name": "box", "time": 1666860582.3565416, "screenSize": [640, 480]}, {"point": [[252, 249], [325, 249], [252, 331], [325, 331]], "name": "box", "time": 1666860582.3567424, "screenSize": [640, 480]}, {"point": [[259, 120], [177, 120], [259, 321], [177, 321]], "name": "box", "time": 1666860582.356877, "screenSize": [640, 480]}, {"point": [[125, 149], [213, 149], [125, 197], [213, 197]], "name": "box", "time": 1666860582.3569944, "screenSize": [640, 480]}, {"point": [[385, 77], [126, 77], [385, 452], [126, 452]], "name": "box", "time": 1666860582.357111, "screenSize": [640, 480]}, {"point": [[266, 51], [92, 51], [266, 314], [92, 314]], "name": "box", "time": 1666860582.3572261, "screenSize": [640, 480]}]
    strings = json.dumps(points)
    do = deal_message()
    ret = do.do_message(json.loads(strings),'run')
    print("end--ret:",ret)