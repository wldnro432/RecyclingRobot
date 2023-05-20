# -*- coding: utf8 -*-
import cv2
import socket
import numpy as np
import time

import threading
import queue

HOST = '192.168.219.103'
PORT = 8486

COMPLETE_DETECT = "9"
STOP_DETECT = "999"
START_DETECT = "111"

flag = False

## TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## server ip, port
s.connect((HOST, PORT))
  
## webcam 이미지 capture
cam = cv2.VideoCapture(0)
 
## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 1680);
cam.set(4, 920);
 
## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    
    if cv2.waitKey(10) == ord("q"):
        flag = True
    elif cv2.waitKey(10) == ord("s"):
        flag = False

    ret, frame = cam.read()
    cv2.imshow("client", frame)
    cv2.waitKey(1)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(frame)
    stringData = data.tobytes()
    
    if flag:
        s.sendall((START_DETECT + str(len(stringData))).encode().ljust(16) + stringData)
    else:
        s.sendall((STOP_DETECT + str(len(stringData))).encode().ljust(16) + stringData)
        
    msg = s.recv(1024).decode()
    print(msg, type(msg))
    