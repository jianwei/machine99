import numpy as np
import cv2
import multiprocessing
import time
 

 
def video_read(camera_id):
    cap = cv2.VideoCapture(camera_id)
    width = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    height = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(width,height)
    while (cap.isOpened()):
        ret,frame = cap.read()
        cv2.imshow('camera', frame )
        key = cv2.waitKey(10)
        if int(key) == 113:
            break
    cap.release()


if __name__ == '__main__':
    print("主进程开始启动！")
    camera_arr = [0,2]
    for item in camera_arr:
        p = multiprocessing.Process(target = video_read, args = (item,))
        p.start()
    print('程序结束！')