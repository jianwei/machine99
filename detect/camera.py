import cv2
import threading

def main(camera_arr):
    for camera_id in camera_arr:
        thread = threading.Thread(target=run_cmd, args=(camera_id,))
        thread.start()


def run_cmd(camera_id):
    cap=cv2.VideoCapture(camera_id) #cv2.VideoCapture(0)代表调取摄像头资源，其中0代表电脑摄像头，1代表外接摄像头(usb摄像头)
    while True:
        success,img=cap.read()
        print(11)
        if success:
            cv2.imshow("Video",img)
        if cv2.waitKey(1)&0xFF==ord('q'):
            break

if __name__ == '__main__':
    camera_arr = [20,22]
    main(camera_arr)