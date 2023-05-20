import time
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np

from numpy import random
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, check_requirements, non_max_suppression, scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized

import socket

import threading
import queue

# SOURCE = 'data/images/bus.jpg'
WEIGHTS = 'best.pt'
IMG_SIZE = 640
DEVICE = ''
AUGMENT = False
CONF_THRES = 0.25
IOU_THRES = 0.45
CLASSES = None
AGNOSTIC_NMS = False

flag = False
label = "9"

START_DETECT = "111"

def detect(img0):
    weights, imgsz = WEIGHTS, IMG_SIZE
    cls_num = 9

    # Initialize
    device = select_device(DEVICE)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

    # Load image
    # img0 = cv2.imread(source, 1)  # BGR
    # assert img0 is not None, 'Image Not Found ' + source

    # Padded resize
    img = letterbox(img0, imgsz, stride=stride)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    t0 = time_synchronized()
    pred = model(img, augment=AUGMENT)[0]

    # Apply NMS
    pred = non_max_suppression(pred, CONF_THRES, IOU_THRES, classes=CLASSES, agnostic=AGNOSTIC_NMS)

    # Process detections
    det = pred[0]

    s = ''
    s += '%gx%g ' % img.shape[2:]  # print string

    if len(det):
        # Rescale boxes from img_size to img0 size
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

        # Print results
        for c in det[:, -1].unique():
            n = (det[:, -1] == c).sum()  # detections per class
            s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

        # Write results
        for *xyxy, conf, cls in reversed(det):
            label = f'{names[int(cls)]} {conf:.2f}'
            cls_num = int(cls)
            plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=3)

    return img0, cls_num

def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def show_image():
    while True:
        img = que2.get()
        cv2.imshow('ImageWindow', img)
        cv2.waitKey(1)

def detect_image():
    while True:
        frame = que.get()
        if flag == True:
            check_requirements(exclude=('pycocotools', 'thop'))
            with torch.no_grad():
                img, label = detect(frame)
        else:
            img = frame
            label = "9"
        que2.put(img)
                # conn.sendall(str(label).encode())

if __name__ == '__main__':

    HOST = '192.168.219.103'
    PORT = 8486

    #TCP 사용
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #서버의 아이피와 포트번호 지정
    s.bind((HOST,PORT))

    # 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
    s.listen(10)

    #연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
    conn,addr=s.accept()

    que = queue.Queue(10)
    que2 = queue.Queue(10)

    t = threading.Thread(target=show_image)
    t2 = threading.Thread(target=detect_image)
    t.start()
    t2.start()

    while True:
        try:
            length = recvall(conn, 16)
            msg = length.decode()[:3]
            stringData = recvall(conn, int(length[3:]))
            data = np.fromstring(stringData, dtype='uint8')
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            que.put(frame)

            print(msg)

            if msg == START_DETECT:
                flag = True
            else:
                flag = False

            conn.sendall(str(label).encode())
        except:
            s.release()
        
        
