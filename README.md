# RecyclingRobot


dataset
  https://drive.google.com/file/d/15uo7mcgeyLsueiHNGoNpMrutypwTf4TU/view


pt
  https://drive.google.com/file/d/1R0cxcW2hDHdkPVM0kpz4cVnGTYJcIIzE/view?usp=share_link
  


![image](https://user-images.githubusercontent.com/124943935/230807139-ca9c444b-24ad-4552-8538-071026e0f4cf.png)



  


train
  !python train.py --device 0 --batch-size 16 --epochs 100 --img 640 640 --data ./data/data/data.yaml --hyp data/hyp.scratch.custom.yaml --cfg cfg/training/yolov7.yaml --weights yolov7.pt --name yolov7-custom

