# RecyclingRobot


dataset
  https://drive.google.com/file/d/15uo7mcgeyLsueiHNGoNpMrutypwTf4TU/view

tree
  


train
  !python train.py --device 0 --batch-size 16 --epochs 100 --img 640 640 --data ./data/data/data.yaml --hyp data/hyp.scratch.custom.yaml --cfg cfg/training/yolov7.yaml --weights yolov7.pt --name yolov7-custom

