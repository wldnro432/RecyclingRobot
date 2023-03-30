import json
import os
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt
import time


start_time = time.time()


try:
    if not os.path.exists("./val_label/"):
        os.makedirs("./val_label/")
except OSError:
    print ('Error: Creating directory. ' +  "./val_label/")

try:
    if not os.path.exists("./val_image/"):
        os.makedirs("./val_image/")
except OSError:
    print ('Error: Creating directory. ' +  "./val_image/")

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


train_root_path = "./Validation/"

image_files = os.listdir('./Validation')
# image_files2 = os.listdir('./Training/[T원천]페트병_기타_기타')
# print(image_files2)

image_file_path = []
label_file_path = []

# Training 
for idx, i in enumerate(image_files):
    # [T원천]종이류_기타_기타 == i 

    # a = [종이류, 기타, 기타]
    a = i.split("]")[1].split("_")
    label_path = a[0]+"/"+a[1]
    # print(i)

    for j in os.listdir(train_root_path+i):
        # 21_X029_C203_1016 == j 
        # print(j)
        
        for k in os.listdir(train_root_path+i+"/"+j):
            # 21_X029_C203_1016_0.JPG   == k
            #            ~
            # 21_X029_C203_1016_5.JPG

            # print(k)

            ## ./Training/[T원천]종이류_기타_기타/21_X029_C203_1016/ 21_X029_C203_1016_0.JPG
            ##                                                               ~
            ##                                                   21_X029_C203_1016_5.JPG
            ## print(train_root_path+i+"/"+j+"/"+k) ## 이미지파일 전체 경로
            image_file_path.append(i+"/"+j+"/"+k)

            ## "./TrainingLabel/"+label_path"/"+i+"/"+j+"/"+k

            label_file_path.append("./ValidationLabel/label/"+label_path+"/"+j+"/"+k[:-4]+".Json")

# print(image_file_path[0])
# print(label_file_path[:10])

print(len(image_file_path))
print(len(label_file_path))

# file = json.load(open("./TrainingLabel/label/페트병/기타/23_X004_C509_0511/23_X004_C509_0511_0.Json"))

# a = ""

for idx, i in tqdm(enumerate(label_file_path)):
    # ./TrainingLabel/label/가구류/기타/1/1_0.json
    file = json.load(open(i))

    # print(idx, i)
    # print(file)

    if file["Bounding"][0]["Drawing"] != "POLYGON":
        name = file["FILE NAME"]
        classes = file["Bounding"][0]["CLASS"]
        x_1 = int(file["Bounding"][0]["x1"])
        y_1 = int(file["Bounding"][0]["y1"])
        x_2 = int(file["Bounding"][0]["x2"])
        y_2 = int(file["Bounding"][0]["y2"])

        img = cv2.imread(train_root_path + image_file_path[idx])
        cv2.imwrite("./val_image/"+image_file_path[idx].split("/")[2], img)

        
        w = int(img.shape[1])
        h = int(img.shape[0])

        b = (x_1, x_2, y_1, y_2)
        bb = convert((w,h), b)

        f = open('./val_label/'+name[:-4]+".txt", 'w')
        f.write("{} {} {} {} {}".format(dict[classes], bb[0], bb[1], bb[2], bb[3]))
        # f.write("{} {} {} {} {}".format(dict[classes], x_1, y_1, x_2, y_2))
        # 파일 닫기
        f.close()
    else:
        print(idx)


print("done")
print(time.time() - start_time)




