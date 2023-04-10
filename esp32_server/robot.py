import RPi.GPIO as GPIO
import time
import threading
import serial
import re
from getkey import getkey
from playsound import playsound
import cv2
import socket
import numpy as np

global distance
### threading 사용 이유는 한 코드 안에서 while문을 여러개 사용하기 위하여!

thread_lock = threading.Lock()

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.07) #0.07
## imu 센서를 시리얼 통신하여 로봇의 방향 데이터를 읽기위함


ARD= serial.Serial("/dev/ttyUSB1",115200,timeout=0.1)
ARD.close()

## 로봇과 esp32의 통신을 위하여 

ARD.open()


### 로봇과 모터신호를 주고 받기 위한 셋팅 

l_encPinA = 14
l_encPinB = 15

r_encPinA = 17
r_encPinB = 27

l_pwmpin = 18
r_pwmpin = 22

l_in1= 23
l_in2= 24

r_in1= 10
r_in2= 9

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(l_encPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(l_encPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r_encPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r_encPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(l_pwmpin,GPIO.OUT)
GPIO.setup(r_pwmpin,GPIO.OUT)

GPIO.setup(l_in1,GPIO.OUT)
GPIO.setup(l_in2,GPIO.OUT)
GPIO.setup(r_in1,GPIO.OUT)
GPIO.setup(r_in2,GPIO.OUT)

l_encoderPos = 0.
r_encoderPos = 0.

one_tic=0.045728 #mm
odom=0
distance=0

mode=0

vel=0.
the=0.

def l_encoderA(channel):
    global l_encoderPos
    global odom
    if GPIO.input(l_encPinA) == GPIO.input(l_encPinB):
        l_encoderPos += 1
        odom+=0.5
    else:
        l_encoderPos -= 1
        odom-=0.5

def l_encoderB(channel):
    global l_encoderPos
    global odom
    if GPIO.input(l_encPinA) == GPIO.input(l_encPinB):
        l_encoderPos -= 1
        odom-=0.5

    else:
        l_encoderPos += 1
        odom+=0.5
def r_encoderA(channel):
    global r_encoderPos
    global odom
    if GPIO.input(r_encPinA) == GPIO.input(r_encPinB):
        r_encoderPos += 1
        odom+=0.5
    else:
        r_encoderPos -= 1
        odom-=0.5

def r_encoderB(channel):
    global r_encoderPos
    global odom
    if GPIO.input(r_encPinA) == GPIO.input(r_encPinB):
        r_encoderPos -= 1
        odom-=0.5
    else:
        r_encoderPos += 1
        odom+=0.5
GPIO.add_event_detect(l_encPinA, GPIO.BOTH, callback=l_encoderA)
GPIO.add_event_detect(l_encPinB, GPIO.BOTH, callback=l_encoderB)
GPIO.add_event_detect(r_encPinA, GPIO.BOTH, callback=r_encoderA)
GPIO.add_event_detect(r_encPinB, GPIO.BOTH, callback=r_encoderB)


def constrain(val, min_val, max_val):

    if val < min_val: return min_val
    if val > max_val: return max_val
    return val

def ahrs():
## 각도 데이터를 읽어 내는 쓰레드
    global yaw

    while True: 

        if ser.readline():
                   
            angle=ser.readline()
            data2 = angle.split(b'\\')
            h=angle.hex()
            k=re.findall(r'5553..................5554',str(h))
 
            if len(k) !=0:
                f=k[0]
                f_yaw=f[12:16]
                YawL=f_yaw[0:2]
                YawH=f_yaw[2:4]

                l=int(YawL,16)
                c=int(YawH,16)

                Yaw=((c<<8)|l)/32768*180
                re_yaw=round(Yaw,1)
                
                if re_yaw >180:
                    re_yaw=re_yaw-360
                    thread_lock.acquire()
                    yaw=re_yaw
                    thread_lock.release()

                thread_lock.acquire()
                yaw=re_yaw
                thread_lock.release()

                ##위는 수정 금지
           
 
def load():
## 이동 경로를 계산하는 스레드
    global odom
    global vel 
    global the
    global mode
    global target_x
    global target_y
    global msg

    point1=0
    point2=0

    current_x=0
    current_y=0

    target_x=0
    target_y=0

    while True:
        
        # print(tcp_msg)
        
        # if msg == '3': ## can

        #     the=0   #앞에보기
        #     s.sendall(code.encode()) # detection 정지
        #     print('can')
        #     time.sleep(10)
        #     ARD.write('j'.encode())    #esp 종이집어라
        #     time.sleep(5)
        #     ARD.write('d'.encode())     #esp 종이 들어라
        #     time.sleep(5)
        #     playsound("종이.mp3")
        #     time.sleep(5)
        #     playsound("물건이동.mp3")
        #     target_x=10 #목표 좌표이동
        #     target_y=10 #목표 좌표이동
        #     time.sleep(10)
        #     the=0   #앞에보기
        #     time.sleep(10)
        #     target_x=0 #홈으로 복귀
        #     target_y=0 #홈으로 복귀
        #     time.sleep(10)
        #     the=0 #앞에봐라
        #     time.sleep(10)
        #     s.sendall(code.encode())


        
        # if msg == '0': ## paper

        #     the=0
        #     s.sendall(code.encode())
        #     print('paper')
        #     time.sleep(10)
        #     ARD.write('j'.encode())
        #     time.sleep(5)
        #     ARD.write('d'.encode())
        #     time.sleep(5)
        #     playsound("종이.mp3")
        #     time.sleep(5)
        #     playsound("물건이동.mp3")
        #     target_x=0
        #     target_y=10
        #     time.sleep(10)
        #     the=0
        #     time.sleep(10)
        #     target_x=0
        #     target_y=0
        #     time.sleep(10)
        #     the=0
        #     time.sleep(10)
        #     s.sendall(code.encode())

        # if msg == '2' :## pet

        #     the=0
        #     s.sendall(code.encode())
        #     print('pet')
        #     time.sleep(10)
        #     ARD.write('j'.encode())
        #     time.sleep(5)
        #     ARD.write('d'.encode())
        #     time.sleep(5)
        #     playsound("종이.mp3")
        #     time.sleep(5)
        #     playsound("물건이동.mp3")
        #     target_x=-10
        #     target_y=10
        #     time.sleep(10)
        #     the=0
        #     time.sleep(10)
        #     target_x=0
        #     target_y=0
        #     time.sleep(10)
        #     the=0
        #     time.sleep(10)
        #     s.sendall(code.encode())

        response = ARD.readline()
        tcp = response[:len(response)-2]

        if tcp == b'target1':
            target_x=-300
            target_y=500
            print('ok')

        if tcp == b'target2':
            target_x=300
            target_y=500
            print('ok')

        if tcp == b'target3':
            target_x=0
            target_y=0
            print('ok')

        if tcp == b'target4':
            target_x=0
            target_y=0
            print('ok')
                
                
        if tcp == b'cider':
            the=-90
            time.sleep(10)
            ARD.write('p'.encode())
            time.sleep(10)
            ARD.write('d'.encode())
            time.sleep(5)
            playsound("물건이동.mp3")

        if tcp == b'cola':
            the=180
            time.sleep(10)
            ARD.write('p'.encode())
            time.sleep(10)
            ARD.write('d'.encode())
            time.sleep(5)
            playsound("물건이동.mp3")

        if tcp == b'fanta':
            the=90
            time.sleep(10)
            ARD.write('p'.encode())
            time.sleep(10)
            ARD.write('d'.encode())
            time.sleep(5)
            playsound("물건이동.mp3")




        distance = odom*0.06
        x_error=target_x-current_x
        y_error=target_y-current_y

        if y_error>0:
            the=0
            time.sleep(3)
            vel=5

            if abs(y_error)<=distance:
                current_y=target_y
                vel=0
                odom=0
                distance=0
                print('ok1')

        if y_error<0:
            the=180
            time.sleep(5)
            vel=5
            
            if abs(y_error)<=distance:
                current_y=target_y
                vel=0
                odom=0
                distance=0
                print('ok2')   

        if x_error>0 and y_error==0:
            the=-90
            time.sleep(5)
            vel=5

            if abs(x_error)<=distance:
                current_x=target_x
                vel=0
                odom=0
                distance=0
                print('ok3')

        if x_error<0 and y_error==0:
            the=90
            time.sleep(5)
            vel=5

            if abs(x_error)<=distance:
                current_x=target_x
                vel=0
                odom=0
                distance=0
                print('ok4')
        else:

            time.sleep(0.01)

def camera():
    #카메라 영상을 서버로 보내는 쓰레드
    global msg

    # -*- coding: utf8 -*-

    ## TCP 사용
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## server ip, port
    s.connect(('192.168.0.20', 8490))
    
    ## webcam 이미지 capture
    cam = cv2.VideoCapture(-1)
    
    ## 이미지 속성 변경 3 = width, 4 = height
    cam.set(3, 1600);
    cam.set(4, 900);
    key=cv2.waitKey(0)


    ## 0~100에서 90의 이미지 품질로 설정 (default = 95)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    
    while True:
   
        # 비디오의 한 프레임씩 읽는다.
        # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
        ret, frame = cam.read()
        # cv2. imencode(ext, img [, params])
        # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        # frame을 String 형태로 변환
        data = np.array(frame)
        stringData = data.tostring()
    
        #서버에 데이터 전송
        #(str(len(stringData))).encode().ljust(16)
        s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
        msg = s.recv(1024).decode("utf-8")
        
        # print(msg)

        if key==ord('q'):
            print('break')
            break


    cam.release()

def keyboard():
    #방향키로 로봇으르 제어하기 위한 스레드
    global vel
    global the
    global distance
    global mode 
    global target_x
    global target_y

    while(True): 


        key = getkey()
        
        if key == 'w':
            vel=vel+2.

        if key == 's':
            vel=vel-2.

        if key == 'a':
            the=the+1

        if key == 'd':
            the=the-1

        if key == 'r':
            vel=0

        if vel <=-50.:
            vel=-50.

        if vel >=50.:
            vel=50.

        if the <-179.9:
            the=180

        if the >180.:
            the=-179.9
        
        if key=='i':
            mode =1

        if key=='o':
            mode =2

        if key=='z':
            thread_lock.acquire()
            target_x=10
            target_y=10
            thread_lock.release()
        if key=='x':
            thread_lock.acquire()
            target_x=-10
            target_y=-10
            thread_lock.release()

        if key =='h':
            ARD.write('j'.encode())     
            time.sleep(5)
            playsound("종이.mp3")
        if key =='j':
            ARD.write('p'.encode())
            time.sleep(5)
            playsound("플라스틱.mp3")
        if key =='k':
            ARD.write('d'.encode())
            time.sleep(5)
            playsound("물건이동.mp3")
        if key =='l':
            ARD.write('q'.encode())

        if key =='n':

            target_x=0
            time.sleep(20)
            target_y=0
     


##로봇의 PID제어        

l_degree=0.
r_degree=0.
yaw_rpm=0.

Kp = 0.005
y_kp=0.27
Ki = 5
y_ki=0.001
Kd = 0.008
y_kd=0.001
dt = 0.

dt_sleep = 0.01
tolerance = 1
start_time = time.time()
l_error_prev = 0.
r_error_prev = 0.
yaw_error_prev=0.

time_prev = 0.
l_errsum = 0.
r_errsum = 0.
yaw_errsum=0.

l_p = GPIO.PWM(18,100)
r_p = GPIO.PWM(22,100)

l_p.start(0)
r_p.start(0)

yaw=0

## 스레드를 실행하는 코드

plan_path=threading.Thread(target=load)
plan_path.start()

imu=threading.Thread(target=ahrs)
imu.start()

key_controll=threading.Thread(target=keyboard)
key_controll.start()

# tcp_camera=threading.Thread(target=camera)
# tcp_camera.start()



## pid 제어 

while True:


    target_l_rpm = vel+l_degree
    target_r_rpm = vel+r_degree

    l_rpm = (60.*l_encoderPos/(dt_sleep*4532.))
    r_rpm = (60.*r_encoderPos/(dt_sleep*4532.))
    
    l_error = abs(target_l_rpm) - abs(l_rpm)
    r_error = abs(target_r_rpm) - abs(r_rpm)
    yaw_error=the-yaw
    
    if abs(yaw_error)>180:
        yaw_error=-(yaw_error/20)
        yaw_error_prev=-(yaw_error_prev)
    l_de = l_error-l_error_prev
    r_de = r_error-r_error_prev
    yaw_de = yaw_error-yaw_error_prev

    dt = time.time() - time_prev
    
    l_errsum=l_errsum+l_error
    r_errsum=r_errsum+r_error
    yaw_errsum=yaw_errsum+yaw_error

    l_control = Kp*l_error + Ki*l_errsum*dt + Kd*l_de/dt
    r_control = Kp*r_error + Ki*r_errsum*dt + Kd*r_de/dt
    yaw_control = y_kp*yaw_error+y_ki*yaw_errsum*dt+y_kd*yaw_de/dt

    r_error_prev = r_error
    yaw_error_prev = yaw_error
    time_prev = time.time()

    l_pwm=constrain(l_control,0,100)
    r_pwm=constrain(r_control,0,100)
    yaw_rpm=constrain(yaw_control,-10,10)

    l_p.ChangeDutyCycle(l_pwm)
    r_p.ChangeDutyCycle(r_pwm)

    l_encoderPos = 0.
    r_encoderPos = 0.
    
    if yaw_rpm >1.5:
        
        l_degree=-yaw_rpm
        r_degree=+yaw_rpm
    
    if yaw_rpm <-1.5:
        
        l_degree=-yaw_rpm
        r_degree=+yaw_rpm

    if -1.5<=yaw_rpm<=1.5:
        l_degree=0.
        r_degree=0.

    if target_l_rpm >= 0:

        GPIO.output(l_in1,0)
        GPIO.output(l_in2,1)

    if target_l_rpm < 0:

        GPIO.output(l_in1,1)
        GPIO.output(l_in2,0)

    if target_r_rpm >= 0:

        GPIO.output(r_in1,1)
        GPIO.output(r_in2,0)

    if target_r_rpm < 0:

        GPIO.output(r_in1,0)
        GPIO.output(r_in2,1)

    time.sleep(dt_sleep)

    