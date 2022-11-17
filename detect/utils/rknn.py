import cv2
import time
import numpy as np
from rknnlite.api import RKNNLite
import yaml
import json
from utils.unix_socket import unix_socket


class RKNNDetector:

    def __init__(self, model_path, config_yaml,to_do):
        self.OBJ_THRESH = 0.25
        self.NMS_THRESH = 0.45
        self.IMG_SIZE = 640
        self.CLASSES = ("box",)
        self.wh = (640, 640)
        self.to_do = to_do
        self._rknn = self.load_rknn_model(model_path)
        self.draw_box = False
        self.inference_time = 0
        self.yolo_time = 0
        self.draw_time = 0
        self.inference_number = 0
        yaml_data = self.get_yaml_data(config_yaml)
        # self.unix_socket = unix_socket(yaml_data.get('unix_socket').get(to_do))
        self.unix_socket = unix_socket(self.get_unix_socket(to_do,yaml_data))

    def get_unix_socket(self,to_do,yaml_config):
        # yaml_config = self.get_yaml_data(config_yaml)
        cameras = yaml_config.get("camera")
        for item in cameras:
            if to_do == item.get("to_do"):
                return item.get("unix_socket")


    def set_screen_size(self, screenSize):
        self.screenSize = screenSize

    def get_yaml_data(self,config_yaml):
        with open(config_yaml, encoding='utf-8')as file:
            content = file.read()
            data = yaml.load(content, Loader=yaml.FullLoader)
            return data

    def load_rknn_model(self, PATH):
        rknn = RKNNLite()
        ret = rknn.load_rknn(PATH)
        if ret != 0:
            print('load rknn model failed')
            exit(ret)
        if self.to_do == "run1":
            ret = rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_0)
        elif self.to_do == "run2":
            ret = rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_1)
        else:
            # ret = rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_0_1)
            ret = rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_2)
        if ret != 0:
            print('Init runtime environment failed')
            exit(ret)
        print('load_rknn_model  done')
        return rknn


    def get_inference_time(self):
        return round(self.avg_inference_time*1000,1)
    
    def get_yolo_time(self):
        return round(self.avg_yolo_time*1000,1)
    
    def get_draw_time(self):
        return round(self.avg_draw_time*1000,1)


    def _predict(self,  _img):
        _img = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        self.inference_number += 1
        t0 = time.time()
        outputs = self._rknn.inference(inputs=[_img])
        t1 = time.time()
        self.inference_time += (t1 - t0)
        self.avg_inference_time = self.inference_time / self.inference_number
        print("inference time:{},avg_inference_time:{}\t".format(
            (t1 - t0), self.avg_inference_time))
        input0_data = outputs[0]
        input1_data = outputs[1]
        input2_data = outputs[2]
        input0_data = input0_data.reshape([3, -1]+list(input0_data.shape[-2:]))
        input1_data = input1_data.reshape([3, -1]+list(input1_data.shape[-2:]))
        input2_data = input2_data.reshape([3, -1]+list(input2_data.shape[-2:]))
        input_data = list()
        input_data.append(np.transpose(input0_data, (2, 3, 0, 1)))
        input_data.append(np.transpose(input1_data, (2, 3, 0, 1)))
        input_data.append(np.transpose(input2_data, (2, 3, 0, 1)))
        boxes, classes, scores = self.yolov5_post_process(input_data)
        t2 = time.time()
        self.yolo_time += t2-t1
        if boxes is not None:
            self.draw(_img, boxes, scores, classes)
        self.draw_time += time.time()-t2
        self.avg_yolo_time = self.yolo_time / self.inference_number
        self.avg_draw_time = self.draw_time / self.inference_number
        return _img

    def draw(self, image, boxes, scores, classes):
        next_data = []
        for box, score, cl in zip(boxes, scores, classes):
            top, left, right, bottom = box
            top = int(top)
            left = int(left)
            right = int(right)
            bottom = int(bottom)
            point = [(top, left), (right, left),
                     (top, bottom), (right, bottom)]
            centery = (left + bottom)/2
            centerx = (top + right)/2
            item = self.get_item_next(self.CLASSES[cl], point,(centerx,centery))
            next_data.append(item)
            msg1 = "{},{}".format(top, left)
            msg2 = "{},{}".format(right, left)
            msg3 = "{},{}".format(top, bottom)
            msg4 = "{},{}".format(right, bottom)
            msg5 = "{},{}".format(centerx, centery)
            cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
            cv2.putText(image, msg1,
                        (top, left),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0,0,255), 2)
            cv2.putText(image, msg2,
                        (right, left),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (255,125,64), 2)
            cv2.putText(image, msg3,
                        (top, bottom),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0,0,255), 2)
            cv2.putText(image, msg4,
                        (right, bottom),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (255,125,64), 2)

            cv2.putText(image, msg5,
                        (int(centerx-20), int(centery)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0,0,0), 2)       
        if (len(next_data) > 0):
            self.send_next(next_data)

    def get_item_next(self, name, point,center):
        next_data = {}
        next_data["point"] = point
        next_data["name"] = name
        next_data["time"] = time.time()
        next_data["center"] = center
        next_data["centerx"] = center[0]
        next_data["centery"] = center[1]
        next_data["screenSize"] = self.screenSize
        return next_data

    def send_next(self, next_data):
        self.unix_socket.send_message(json.dumps(next_data))

    def yolov5_post_process(self, input_data):
        masks = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        anchors = [[10, 13], [16, 30], [33, 23], [30, 61], [62, 45],
                   [59, 119], [116, 90], [156, 198], [373, 326]]
        boxes, classes, scores = [], [], []
        for input, mask in zip(input_data, masks):
            b, c, s = self.process(input, mask, anchors)
            b, c, s = self.filter_boxes(b, c, s)
            boxes.append(b)
            classes.append(c)
            scores.append(s)
        boxes = np.concatenate(boxes)
        boxes = self.xywh2xyxy(boxes)
        classes = np.concatenate(classes)
        scores = np.concatenate(scores)
        nboxes, nclasses, nscores = [], [], []
        for c in set(classes):
            inds = np.where(classes == c)
            b = boxes[inds]
            c = classes[inds]
            s = scores[inds]

            keep = self.nms_boxes(b, s)

            nboxes.append(b[keep])
            nclasses.append(c[keep])
            nscores.append(s[keep])
        if not nclasses and not nscores:
            return None, None, None
        boxes = np.concatenate(nboxes)
        classes = np.concatenate(nclasses)
        scores = np.concatenate(nscores)
        return boxes, classes, scores

    def nms_boxes(self, boxes, scores):
        x = boxes[:, 0]
        y = boxes[:, 1]
        w = boxes[:, 2] - boxes[:, 0]
        h = boxes[:, 3] - boxes[:, 1]
        areas = w * h
        order = scores.argsort()[::-1]
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x[i], x[order[1:]])
            yy1 = np.maximum(y[i], y[order[1:]])
            xx2 = np.minimum(x[i] + w[i], x[order[1:]] + w[order[1:]])
            yy2 = np.minimum(y[i] + h[i], y[order[1:]] + h[order[1:]])
            w1 = np.maximum(0.0, xx2 - xx1 + 0.00001)
            h1 = np.maximum(0.0, yy2 - yy1 + 0.00001)
            inter = w1 * h1
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= self.NMS_THRESH)[0]
            order = order[inds + 1]
        keep = np.array(keep)
        return keep

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def xywh2xyxy(self, x):
        y = np.copy(x)
        y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
        y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
        y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
        y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
        return y

    def filter_boxes(self, boxes, box_confidences, box_class_probs):
        boxes = boxes.reshape(-1, 4)
        box_confidences = box_confidences.reshape(-1)
        box_class_probs = box_class_probs.reshape(-1,
                                                  box_class_probs.shape[-1])
        _box_pos = np.where(box_confidences >=
                            self.OBJ_THRESH)  # 找出概率大于阈值的item
        boxes = boxes[_box_pos]
        box_confidences = box_confidences[_box_pos]
        box_class_probs = box_class_probs[_box_pos]
        class_max_score = np.max(box_class_probs, axis=-1)
        classes = np.argmax(box_class_probs, axis=-1)
        _class_pos = np.where(class_max_score >= self.OBJ_THRESH)
        boxes = boxes[_class_pos]
        classes = classes[_class_pos]
        scores = (class_max_score * box_confidences)[_class_pos]
        return boxes, classes, scores

    def process(self, input, mask, anchors):
        anchors = [anchors[i] for i in mask]
        grid_h, grid_w = map(int, input.shape[0:2])
        box_confidence = self.sigmoid(input[..., 4])
        box_confidence = np.expand_dims(box_confidence, axis=-1)
        box_class_probs = self.sigmoid(input[..., 5:])
        box_xy = self.sigmoid(input[..., :2])*2 - 0.5
        col = np.tile(np.arange(0, grid_w), grid_w).reshape(-1, grid_w)
        row = np.tile(np.arange(0, grid_h).reshape(-1, 1), grid_h)
        col = col.reshape(grid_h, grid_w, 1, 1).repeat(3, axis=-2)
        row = row.reshape(grid_h, grid_w, 1, 1).repeat(3, axis=-2)
        grid = np.concatenate((col, row), axis=-1)
        box_xy += grid
        box_xy *= int(self.IMG_SIZE/grid_h)
        box_wh = pow(self.sigmoid(input[..., 2:4])*2, 2)
        box_wh = box_wh * anchors
        box = np.concatenate((box_xy, box_wh), axis=-1)
        return box, box_confidence, box_class_probs

    def predict_resize(self, img_src, conf_thres=0.4, iou_thres=0.45):
        _img = cv2.resize(img_src, self.wh)
        gain = img_src.shape[:2][::-1]
        return self._predict(img_src, _img, gain, conf_thres, iou_thres, )

    def letterbox(self, img, new_wh=(416, 416), color=(114, 114, 114)):
        a = AutoScale(img, *new_wh)
        new_img = a.new_img
        h, w = new_img.shape[:2]
        new_img = cv2.copyMakeBorder(
            new_img, 0, new_wh[1] - h, 0, new_wh[0] - w, cv2.BORDER_CONSTANT, value=color)
        return new_img, (new_wh[0] / a.scale, new_wh[1] / a.scale)

    def predict(self, img_src, conf_thres=0.4, iou_thres=0.45):
        _img, gain = self.letterbox(img_src, self.wh)
        return self._predict(_img)

    def close(self):
        self._rknn.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    # def show_top5(result):
    #     output = result[0].reshape(-1)
    #     # softmax
    #     output = np.exp(output)/sum(np.exp(output))
    #     output_sorted = sorted(output, reverse=True)
    #     top5_str = 'resnet18\n-----TOP 5-----\n'
    #     for i in range(5):
    #         value = output_sorted[i]
    #         index = np.where(output == value)
    #         for j in range(len(index)):
    #             if (i + j) >= 5:
    #                 break
    #             if value > 0:
    #                 topi = '{}: {}\n'.format(index[j], value)
    #             else:
    #                 topi = '-1: 0.0\n'
    #             top5_str += topi
    #     print(top5_str)


class AutoScale:
    def __init__(self, img, max_w, max_h):
        self._src_img = img
        self.scale = self.get_max_scale(img, max_w, max_h)
        self._new_size = self.get_new_size(img, self.scale)
        self.__new_img = None

    def get_max_scale(self, img, max_w, max_h):
        h, w = img.shape[:2]
        scale = min(max_w / w, max_h / h, 1)
        return scale

    def get_new_size(self, img, scale):
        return tuple(map(int, np.array(img.shape[:2][::-1]) * scale))

    @property
    def size(self):
        return self._new_size

    @property
    def new_img(self):
        if self.__new_img is None:
            self.__new_img = cv2.resize(self._src_img, self._new_size)
        return self.__new_img
