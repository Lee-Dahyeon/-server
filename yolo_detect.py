import torch
import numpy as np
import yaml

class ImageDetect:
    model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5s', force_reload=True)
    data={}
    
    # 클래스 생성 시 자동으로 호출되는 생성자 함수
    def __init__(self):
        with open('coco.yaml','r', encoding='UTF-8') as f:
            self.data=yaml.full_load(f)['names']
    
    # self 쓰는 이유: 클래스 내에 정의되어 있는 함수라는 것, 클래스 이름을 가르키는 키워드
    def detect_img(self, img):
        result=self.model(img).xyxyn[0].numpy() #ImageDetect안에 있는 변수를 가져온다는 것을 의미
        return result