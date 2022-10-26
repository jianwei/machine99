from utils.rknn import RKNNDetector 
import cv2
import time,os




if __name__ == '__main__':
    filt_folder = os.getcwd()
    print("filt_folder:",filt_folder)
    RKNN_MODEL_PATH = filt_folder + "/weight/box.rknn"
    print("RKNN_MODEL_PATH:",RKNN_MODEL_PATH)
    detector = RKNNDetector(RKNN_MODEL_PATH)
    cap=cv2.VideoCapture(20)

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

