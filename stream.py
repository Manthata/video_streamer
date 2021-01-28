#!/usr/bin/env python
import time
import argparse
import socketio as socketio
import cv2
import base64
import os
from importlib import import_module
from datetime import datetime as d
from pymongo import MongoClient
import gridfs
import json
import bsonjs
from datetime import datetime as d
from flask import jsonify
import requests
import numpy as np 




import sys
sys.path.append(".")


# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
    print("Load module {}".format('camera_' + os.environ['CAMERA']))
else:
    from camera import Camera

uri = os.environ.get('URI')
client = MongoClient(uri)
db = client.coords
coords = db["Coords"]


def save(encoded_data, filename):
    nparr = np.fromstring(encoded_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    # cv2.imshow("img", img)
    return cv2.imwrite(filename, img)

def write_string(text):
    path = os.getcwd()
    myText = open( r'path\name.txt', 'w')
    myText.write(text)
    myText.close()


class CVClient(object):
    def __init__(self):
        self.server_port = 5001
        self._last_update_t = time.time()
       

    # the setup function
    def setup(self):
        print("[INFO] connecting to the database....")
        return self

    def image_to_jpeg(self, frame):
        buffer = cv2.imencode('.jpg', frame)[1]
        image_str = base64.b64encode(buffer).decode('utf-8', 'ignore')
        image_str_data = json.dumps("{}".format(image_str))

        #the image string with charectors decode
        # image_str = base64.b64encode(buffer).decode('utf-8', 'ignore')

        # format to display on the web "data:image/jpeg;base64,{}".format(image_str)


        return image_str_data

    #send the data to the server
    def send_data(self, frame):
        image_str = self.image_to_jpeg(frame)
        # frame = self.image_to_jpeg(frame)
        
        resp = requests.post('http://localhost:5000/save_video', json = {"frame": image_str})

        if resp.status_code != 200:
            print('POST status code: {}'.format(resp.status_code))
        

    def save_box_data(self, tracked_objects):
        date = d.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        data = json.dumps(tracked_objects)
        coords.insert_one({
            "timestamp": date,
            "points": data ,
            
        })


def main():
    try : 
        streamer = CVClient().setup()
     
        while True:
            frame, tracks = Camera().get_frame()
            streamer.send_data(frame)
            streamer.save_box_data(tracks)
            
    
    finally:

        if Camera._thread() == "Stopping camera thread due to inactivity.":
            frame = Camera().get_frame()
            streamer.send_data(frame)
            #
            # streamer.save_data(frame)
            streamer.save_box_data(tracks)



if __name__ == "__main__":
    main()
