import json
import random
import os
from tqdm import tqdm

import cv2
import matplotlib.pyplot as plt

import time

start_time = time.time()

try:
    if not os.path.exists("./train/label/"):
        os.makedirs("./train/label/")
    if not os.path.exists("./train/image/"):
        os.makedirs("./train/image/")
    if not os.path.exists("./valid/label/"):
        os.makedirs("./valid/label/")
    if not os.path.exists("./valid/image/"):
        os.makedirs("./valid/image/")
except OSError:
    print ('Error: Creating directory. ' +  "./label/")

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = ( box[0] + box[1] ) / 2.0
    y = ( box[2] + box[3] ) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

dict = {"종이류":0,
    "페트병류":1,
    "플라스틱류":2,
    "캔류":3,
    "유리류":4,
    "비닐류":5
    }

train_root_path = "./Training/"
image_files = os.listdir('./Training')

image_file_path = []
label_file_path = []

# Training 
for idx, i in enumerate(image_files):
    # [T원천]종이류_기타_기타 == i 

    # a = [종이류, 기타, 기타]
    a = i.split("]")[1].split("_")
    label_path = a[0]+"/"+a[1]

    for j in os.listdir(train_root_path+i):
        # 21_X029_C203_1016 == j 
        
        for k in os.listdir(train_root_path+i+"/"+j):
            # 21_X029_C203_1016_0.JPG   == k
            #            ~
            # 21_X029_C203_1016_5.JPG

            ## ./Training/[T원천]종이류_기타_기타/21_X029_C203_1016/ 21_X029_C203_1016_0.JPG
            ##                                                               ~
            ##                                                   21_X029_C203_1016_5.JPG
            ## print(train_root_path+i+"/"+j+"/"+k) ## 이미지파일 전체 경로
            image_file_path.append(i+"/"+j+"/"+k)
            label_file_path.append("./TrainingLabel/label/"+label_path+"/"+j+"/"+k[:-4]+".Json")


error_list = []

# a = random.shuffle(label_file_path)

random.shuffle(label_file_path)

for idx, i in tqdm(enumerate(label_file_path[:500])):
    # ./TrainingLabel/label/가구류/기타/1/1_0.json
    
    file = json.load(open(i))
    
    if file["Bounding"][0]["Drawing"] != "POLYGON":
        name = file["FILE NAME"]
        classes = file["Bounding"][0]["CLASS"]
        if idx % 5 == 0:
            print(classes)
        x_1 = int(file["Bounding"][0]["x1"])
        y_1 = int(file["Bounding"][0]["y1"])
        x_2 = int(file["Bounding"][0]["x2"])
        y_2 = int(file["Bounding"][0]["y2"])

        a = i.split("/")
        img = cv2.imread(train_root_path + "[T원천]"+a[3]+"_"+a[4]+"_"+a[4]+"/"+a[5]+"/"+a[6][:-5]+".jpg")

        w = int(img.shape[1])
        h = int(img.shape[0])

        b = (x_1, x_2, y_1, y_2)
        bb = convert((w,h), b)
        
        if idx % 2 == 0:
            cv2.imwrite("./train/image/"+a[6][:-5]+".jpg", img)

            f = open('./train/label/'+name[:-4]+".txt", 'w')
            f.write("{} {} {} {} {}".format(dict[classes], bb[0], bb[1], bb[2], bb[3]))
        else:
            cv2.imwrite("./valid/image/"+a[6][:-5]+".jpg", img)

            f = open('./valid/label/'+name[:-4]+".txt", 'w')
            f.write("{} {} {} {} {}".format(dict[classes], bb[0], bb[1], bb[2], bb[3]))

        f.close()
            
    else:
        error_list.append(idx)


print(error_list)

print("missing :", len(error_list))
print("complete : ", len(image_files) - len(error_list))

print("done")
print(time.time() - start_time)    
