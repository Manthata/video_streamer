from models import *
import sys
sys.path.insert(1, './utils')
from utils import *
from torch.utils.data import DataLoader
import cv2
from sort import *
import numpy as np
import pandas as pd 
from detect import detect_image
from myUtils import intersect
import requests 


config_path = '/config/yolov3.cfg'
weights_path='config/yolov3.weights'
class_path='config/coco.names'
img_size =416
conf_thres=0.8
nms_thres=0.4
classes = utils.load_classes(class_path)
colors=[(255,0,0),(0,255,0),(0,0,255),(255,0,255),(128,0,0),(0,128,0),(0,0,128),(128,0,128),(128,128,0),(0,128,128)]


vid_source = "input/example_01.mp4"
vid = cv2.VideoCapture(0)
mot_tracker = Sort()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
ret, frame = vid.read()
#print(cap.shape)
#frame = cv2.resize(cap, (500, 500))
vw = frame.shape[1]
vh = frame.shape[0]
# print(frame.shape)
# print ("Video size", vh,vw)


frame_out = cv2.VideoWriter("outputs/frame_201.mp4",fourcc,20.0,(vw,vh))

all_lines = {}
all_lines_transformed = {}
frames = 0
starttime = time.time()

while(True):
    ret, frame = vid.read()
    if not ret:
        break
    frames += 1
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(frame)
    detections = detect_image(pilimg)
    # print("we are in the first part of the while frame ")

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    img = np.array(pilimg)
    pad_x = max(img.shape[0] - img.shape[1], 0) * (img_size / max(img.shape))
    pad_y = max(img.shape[1] - img.shape[0], 0) * (img_size / max(img.shape))
    unpad_h = img_size - pad_y
    unpad_w = img_size - pad_x
    if detections is not None:
        tracked_objects = mot_tracker.update(detections.cpu())

        unique_labels = detections[:, -1].cpu().unique()
        n_cls_preds = len(unique_labels)
        for x1, y1, x2, y2, obj_id, cls_pred in tracked_objects:
            box_h = int(((y2 - y1) / unpad_h) * img.shape[0])
            box_w = int(((x2 - x1) / unpad_w) * img.shape[1])
            y1 = int(((y1 - pad_y // 2) / unpad_h) * img.shape[0])
            x1 = int(((x1 - pad_x // 2) / unpad_w) * img.shape[1])
            color = colors[int(obj_id) % len(colors)]
            cls = classes[int(cls_pred)]
            cv2.rectangle(frame, (x1, y1), (x1+box_w, y1+box_h), color, 4)
            cv2.rectangle(frame, (x1, y1-35),
                          (x1+len(cls)*19+80, y1), color, -1)
            cv2.putText(frame, cls + "-" + str(int(obj_id)), (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
            if not obj_id in all_lines:
                all_lines[obj_id] = []

            cord = all_lines[obj_id]
            # reduce the length of the line
            #if len(cord) > 50:
                #cord.pop(0)

            #x1 = int(x1 + box_w/2)
            #y1 = int(y1 +box_h/2)
            x1 = int(x1 + box_w/2)
            y1 = int(y1 + box_h/2)
            

            cv2.circle(frame, (x1, y1), 5,color , -1)
            cord.append((x1,y1))
            y = []
            x = []
            for i in cord:
                y.append(i[1])
                x.append(i[0])
           
            for index, xp in enumerate(cord[:-1]):
                cv2.line(frame, xp, cord[index + 1], color, 5, lineType=8)
            
            
            

    cv2.line(frame, (0, 100), (1277, 100), (0, 0, 255),
             thickness=4, lineType=8, shift=0)
             
    cv2.imshow('Stream_1', frame)
    ch = 0xFF & cv2.waitKey(1)
    if ch == 27:
        break

totaltime = time.time()-starttime
print(frames, "frames", (totaltime/frames), "frame/s")
cv2.destroyAllWindows()
frame_out.release()
