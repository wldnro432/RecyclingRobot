# -*- coding: utf8 -*-
import cv2
import socket
import numpy as np
import time

HOST = '192.168.0.20'
PORT = 8765


COMPLETE_DETECT = "9"
STOP_DETECT = "999"
START_DETECT = "111"

flag = True
 
## TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## server ip, port
s.connect((HOST, PORT))
  
## webcam 이미지 capture
cam = cv2.VideoCapture(0)
 
## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 1600);
cam.set(4, 960);
 
## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
 
while True:

    # 비디오의 한 프레임씩 읽는다.
    # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
    ret, frame = cam.read()
    # cv2. imencode(ext, img [, params])
    # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    # frame을 String 형태로 변환
    data = np.array(frame)
    stringData = data.tobytes()
    #서버에 데이터 전송
    #(str(len(stringData))).encode().ljust(16)




    
    # s.sendall((str(len(stringData))).encode().ljust(16) + stringData)

    
    # if flag:de().ljust(16) + stringData)
    #     # s.sendall(STOP_DETECT.encode().ljust(16) + stringData)

    #     s.sendall((START_DETECT + str(len(stringData[3:]))).encode().ljust(16) + stringData)
    #     # s.sendall(START_DETECT.encode().ljust(16) + stringData)
    #     # 
    #     # if msg == COMPLETE_DETECT:  k 
    #     #     s.send((STOP_DETECT + str(len(stringData[4:]))).encode().ljust(16) + stringData)
    # else:
    #     s.sendall((STOP_DETECT + str(len(stringData[3:]))).enco

    

    msg = s.recv(1024).decode()
    print(msg, type(msg))

    
    if msg == COMPLETE_DETECT:
        flag = True
    else:
        flag = False

    print(flag)


    if flag:
        s.sendall((START_DETECT + str(len(stringData))).encode().ljust(16) + stringData)
        
    else:
        s.sendall((STOP_DETECT + str(len(stringData))).encode().ljust(16) + stringData)
        
    



    
    
    # key = cv2.waitKey(1) 

    # if key == ord("q"):
    #     flag = True
    # elif key == ord("s"):
    #     cam.release()
    #     break