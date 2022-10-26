from utils.rknn import RKNNDetector 
import cv2
import time,os
import argparse


def main(camera_id):
    filt_folder = os.getcwd()
    RKNN_MODEL_PATH = filt_folder + "/weights/box.rknn"
    detector = RKNNDetector(RKNN_MODEL_PATH)
    
    cap=cv2.VideoCapture(camera_id)
    while True:
        print("--------------------------------------------------------------------------------------------------")
        t0 = time.time()
        success,img=cap.read()
        src_h, src_w = img.shape[:2]
        img_1 = detector.predict(img)
        t1 = time.time()
        fps = round(1/(t1-t0),3)
        cv2.putText(img_1,"fps:{}".format(fps), (0,30),0,1,(0, 0, 255),thickness=2,lineType=cv2.LINE_AA)
        print("width:{},height:{},fps:{}".format(src_w,src_h,fps) )
        cv2.imshow("Video",img_1)
        if cv2.waitKey(1)&0xFF==ord('q'):
            break




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera_id', nargs='+', type=str, default= '20', help='model path or triton URL')
    opt = parser.parse_args()
    print(opt,type(opt))
    main(**vars(opt))
    pass

