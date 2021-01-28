from flask import jsonify
from detect import detect_image
import numpy as np
from sort import *
from torch.utils.data import DataLoader
from utils import *
from base_camera import BaseCamera
import cv2
import base64
from models import *
import sys
sys.path.insert(1, './utils')
import pandas as pd


mot_tracker = Sort()
class Camera(BaseCamera):

    @staticmethod
    def frames():

        while True:

            # cam = cv2.VideoCapture("video.MOV")
            vid_source = "input/example_01.mp4"
            cap = cv2.VideoCapture(0)
            # finds the frame width automatically
            # frame_width = int(cap.get(3))
            # frame_height = int(cap.get(4))
            # cam = cv2.VideoCapture(0)


            assert cap.isOpened(), "Can not open video file."

            while True:
                ret, frame = cap.read()

                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pilimg = Image.fromarray(frame)
                    detections = detect_image(pilimg)
                    tracked_objects = []
                    if detections is not None:
                        tracked_objects.append(mot_tracker.update(detections.cpu()))
                        
                        print("[INFO]: tracked objects", tracked_objects)
                        # resize the frame to 0.5x
                                                           
                    #jpg_as_text=base64.b64encode(buffer)
                    tracks = pd.Series(tracked_objects).to_json(orient='values')
                    #

                    # encode as a jpeg image and return it
                    yield frame, tracks
                else:
                    break
