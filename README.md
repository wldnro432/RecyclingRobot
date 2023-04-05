# RecyclingRobot


dataset
  https://drive.google.com/file/d/15uo7mcgeyLsueiHNGoNpMrutypwTf4TU/view


pt
  https://drive.google.com/file/d/1wtNzLqln_Py9v_ra0Ffp-FnSqFo5DD3Y/view?usp=share_link
  


tree
yolov7
├── cfg
│   ├── baseline
│   ├── deploy
│   └── training
│       └── yolov7.yaml
├── data
│   ├── test
│   │   ├── images
│   │   └── labels
│   ├── train
│   │   ├── images
│   │   └── labels
│   └── valid
│   │   ├── images
│   │   └── labels
│   │── data.yaml
│   └── hyp.scratch.custom.yaml
│
├──train.py
├──yolov7.pt


  


train
  !python train.py --device 0 --batch-size 16 --epochs 100 --img 640 640 --data ./data/data/data.yaml --hyp data/hyp.scratch.custom.yaml --cfg cfg/training/yolov7.yaml --weights yolov7.pt --name yolov7-custom

