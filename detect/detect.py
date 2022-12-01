from utils.rknn import RKNNDetector 
import cv2
import time,os,json
import argparse

def main(camera_id,save_video=False,to_do="run"):
    filt_folder = os.getcwd()
    # RKNN_MODEL_PATH = filt_folder + "/weights/chives.rknn"
    RKNN_MODEL_PATH = filt_folder + "/weights/corn.rknn"
    detector = RKNNDetector(RKNN_MODEL_PATH,'../config.yaml',to_do)
    
    cap = cv2.VideoCapture(camera_id)
    # cap.set(3, 720)
    # cap.set(4, 480)
    if save_video:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #对视频设置的编码解码的方式MPEG-4编码
        fource=cv2.VideoWriter_fourcc(*'DIVX')
        video_path = './run/source/{}.mp4'.format(to_do+"_"+str(now_time))
        source_video=cv2.VideoWriter(video_path,fource,12,(640,480))
        inference_path = './run/inference/{}.mp4'.format(to_do+"_"+str(now_time))
        inference_video=cv2.VideoWriter(inference_path,fource,12,(640,640))
    total_frame,totao_fps,t01,success,img,src_h, src_w,img_1,avg_inference_time,avg_yolo_time,t1,fps,avg_fps,t02,min,second = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    t01 = time.time()
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

            next_data_reasult = detector.next_data_ret
            print("next_data_ret:",next_data_reasult)
            debug_draw_line(next_data_reasult,img_1)
            # debug_NPU_load(img_1,src_w,src_h)

            avg_inference_time = detector.get_inference_time()
            avg_yolo_time = detector.get_yolo_time()
            # avg_draw_time = detector.get_draw_time()
            t1 = time.time()
            fps = round(1/(t1-t0),2)
            totao_fps += fps
            avg_fps = round(totao_fps/total_frame,2)
            t02 = time.time()
            min = int((t02-t01)/60)
            second = int((t02-t01)%60)
            tmp_cmd = 'cat /sys/class/thermal/thermal_zone0/temp'
            val = os.popen(tmp_cmd)
            tmp = int(int(val.read())/1000)
            # print(tmp)
            cv2.putText(img_1,"avg_fps: {}, run: {}:{}, infer: {},yolo:{},tmp:{}".format(avg_fps,min,second,avg_inference_time,avg_yolo_time,tmp), (0,20),0,0.6,(0, 0, 255),thickness=2,lineType=cv2.LINE_AA)
            cv2.putText(img_1,"cur_fps:{}".format(fps), (0,src_h-10),0,0.6,(0, 0, 255),thickness=2,lineType=cv2.LINE_AA)

            cv2.putText(img_1,"L".format(fps), (0,int(src_h/2)),0,1,(0, 255, 255),thickness=2,lineType=cv2.LINE_AA)
            cv2.putText(img_1,"R".format(fps), (src_w-20,int(src_h/2)),0,1,(0, 255, 255),thickness=2,lineType=cv2.LINE_AA)




            cv2.line(img_1,(int(src_w/2),0),(int(src_w/2),int(src_h)),(0,255,255),2)
            cv2.imshow("3588_{}_inference_video".format(to_do),img_1)
            if save_video:
                inference_video.write(img_1)
            if cv2.waitKey(1)&0xFF==ord('q'):
                if save_video:
                    print("save video to:{},inference_path:{}".format(video_path,inference_path))
                break


def debug_NPU_load(img_1,src_w,src_h):
    tmp_cmd = 'sudo cat /sys/kernel/debug/rknpu/load'
    val = os.popen(tmp_cmd)
    print("NPU:{}".format(val))
    # cv2.putText(img_1,"{}".format(val), (int(src_w/2-20),src_h-10),0,0.6,(0, 255, 255),thickness=2,lineType=cv2.LINE_AA)

def debug_draw_line(ret,img_1):
    # print("ret:",ret)
    lines  = json.loads(ret).get("lines_format")
    reasult  = json.dumps(json.loads(ret).get("reasult"))
    # print("lines:",lines)
    for line in lines:
        if (len(line)>1):
            for i in range(len(line)):
                if (i!=len(line)-1):
                    item = line[i]
                    next_item = line[i+1]
                    center = item.get("center")
                    next_center = next_item.get("center")
                    # print("center:{},{},{},next_center:{},{},{}".format(center,int(center[0]),int(center[1]),next_center,int(next_center[0]),int(next_center[1])))
                    cv2.line(img_1,(int(center[0]),int(center[1])),(int(next_center[0]),int(next_center[1])),(227,207,87),2)
                    # cv2.line(img_1,(int(center[0]),int(center[1])),(320,480),(227,7,87),2)
    cv2.putText(img_1,reasult, (620,250),0,1,(0, 255, 255),thickness=2,lineType=cv2.LINE_AA)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera_id',  type=int, default=20, help='model path or triton URL')
    parser.add_argument('--save_video', action='store_true', help='do not save images/videos')
    parser.add_argument('--to_do', type=str,default="run", help='run or work')
    opt = parser.parse_args()
    main(**vars(opt))
    
    