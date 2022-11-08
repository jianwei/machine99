import numpy as np
import multiprocessing
from utils.rknn import RKNNDetector
import cv2
import time
import os
import argparse


def main(camera_id):
    video_read(camera_id)
    pass


def video_read(camera_id):
    
    # width = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    # height = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # print(camera_id, width, height)
    to_do ="run" if camera_id == 20 else "work"
    filt_folder = os.getcwd()
    RKNN_MODEL_PATH = filt_folder + "/weights/box.rknn"
    detector = RKNNDetector(RKNN_MODEL_PATH,'../config.yaml',to_do)

    cap = cv2.VideoCapture(camera_id)
    total_frame,totao_fps,t01,success,img,src_h, src_w,img_1,avg_inference_time,avg_yolo_time,avg_draw_time,t1,fps,avg_fps,t02,min,second = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    t01 = time.time()

    while (cap.isOpened()):
        ret, img = cap.read()
        src_h, src_w = img.shape[:2]
        detector.set_screen_size((src_w,src_h))
        img_1 = detector.predict(img)

        cv2.imshow('camera', img_1)
        key = cv2.waitKey(10)
        if int(key) == 113:
            break
    cap.release()


if __name__ == '__main__':
    print("主进程开始启动！")
    camera_arr = [20, 22]
    for item in camera_arr:
        p = multiprocessing.Process(target=main, args=(item,))
        p.start()
    print('程序结束！')
