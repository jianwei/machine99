from utils.rknn import RKNNDetector 
import cv2
import time,os
import argparse


def main(camera_id,save_video=False,to_do="run"):
    filt_folder = os.getcwd()
    RKNN_MODEL_PATH = filt_folder + "/weights/box.rknn"
    detector = RKNNDetector(RKNN_MODEL_PATH,'../config.yaml',to_do)
    print("save:",save_video)

    cap=cv2.VideoCapture(camera_id)
    if save_video:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #对视频设置的编码解码的方式MPEG-4编码
        fource=cv2.VideoWriter_fourcc(*'DIVX')
        video_path = './run/source/{}.mp4'.format(to_do+"_"+str(now_time))
        source_video=cv2.VideoWriter(video_path,fource,20,(640,480))
        # inference_video=cv2.VideoWriter('./run/inference/{}.mp4'.format(now_time),fource,20,(640,480))
    total_frame = 0
    totao_fps=0
    while True:
        print("--------------------------------------------------------------------------------------------------")
        total_frame+=1
        t0 = time.time()
        success,img=cap.read()
        if save_video:
            source_video.write(img)
        if success:
            src_h, src_w = img.shape[:2]
            detector.set_screen_size((src_w,src_h))
            img_1 = detector.predict(img)
            t1 = time.time()
            fps = round(1/(t1-t0),3)
            totao_fps += fps
            avg_fps = round(totao_fps/total_frame,3)
            cv2.putText(img_1,"FPS:{},avg Fps:{}".format(fps,avg_fps), (0,30),0,1,(0, 0, 255),thickness=2,lineType=cv2.LINE_AA)
            # print("width:{},height:{},fps:{}".format(src_w,src_h,fps) )
            cv2.imshow("3588_run_inference_video",img_1)
            if cv2.waitKey(1)&0xFF==ord('q'):
                if save_video:
                    print("save video to:{}".format(video_path))
                break




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera_id',  type=int, default=20, help='model path or triton URL')
    parser.add_argument('--save_video', action='store_true', help='do not save images/videos')
    parser.add_argument('--to_do', type=str,default="run", help='run or work')
    opt = parser.parse_args()
    # print(opt,type(opt))
    main(**vars(opt))
    pass

