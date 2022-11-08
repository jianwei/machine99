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
    cap = cv2.VideoCapture(camera_id)
    width = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    height = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(camera_id, width, height)
    while (cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('camera', frame)
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
