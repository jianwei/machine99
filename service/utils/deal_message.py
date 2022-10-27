import json
# import redis_connect
import time
import threading
# import work


class deal_message():

    def __init__(self):
        # self.redis = redis_connect()
        self.work_thread = ""
        # self.work = work(self.redis)

    def do_message(self, message):
        if (message):
            return "do_message finish"
            # self.get_common_data(message)
            # self.redis.set(message)
            # message = json.loads(message)
            # if (message["is_synchro"]):
            #     pass
            # else:
            #     self.work_thread = threading.Thread(target=self.work.do, args=())
            #     self.work_thread.start()

    def get_common_data(self, message):
        point = message["point"]
        message["centerx"] = (point[0][0] + point[1][0])/2
        message["centery"] = (point[0][1] + point[2][1])/2
        message["center"] = [message["centerx"], message["centery"]]
        return message
