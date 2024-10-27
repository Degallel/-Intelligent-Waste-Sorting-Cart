import cv2
import os
import time
import logging

from ultralytics import YOLO
from PIL import Image

logger = logging.getLogger(__name__)

def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height


def detect_objects_with_custom_model(image_path, model_path):
    #  YOLOv8 模型
    model = YOLO(model_path)  
    

    image_width, image_height = get_image_size(image_path)
    

    results = model(image_path)
    
    # 获取推理结果
    output = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # 边界框坐标
        confidences = result.boxes.conf.cpu().numpy()  # 置信度
        labels = result.boxes.cls.cpu().numpy()  # 标签索引
        
        # 类别名称
        class_names = model.names  
        detected_labels = [class_names[int(label)] for label in labels]
        
        for label, confidence, box in zip(detected_labels, confidences, boxes):
            xmin, ymin, xmax, ymax = box
            
            # 计算中心坐标
            center_x = (xmin + xmax) / 2
            center_y = (ymin + ymax) / 2
            
            
            # 进行坐标归一化
            xmin_norm = xmin / image_width
            ymin_norm = ymin / image_height
            xmax_norm = xmax / image_width
            ymax_norm = ymax / image_height
            center_x_norm = center_x / image_width
            center_y_norm = center_y / image_height

            
            # 保存结果
            output.append({
                'label': label,
                'confidence': round(float(confidence), 2),
                'box_normalized': [round(xmin_norm, 4), round(ymin_norm, 4), round(xmax_norm, 4), round(ymax_norm, 4)],
                'center_normalized_x': round(center_x_norm, 4),
                'center_normalized_y': round(center_y_norm, 4),
                'area_box': (ymax - ymin)*(xmax - xmin)
            })
    results[0].show() #图片显示
    return output

class yolo:
    def __init__(self):
        self.enter_x = 0
        self.enter_y = 0
        self.model_path = '/home/pi/new3.pt'
        self.status = 'stay'
        self.label = None
        self.wait = 0

    def run(self, total_status):
        if total_status == None:
            self.status == 'stay'
            return None, None, None, self.status

        if total_status == 'yolo':
            self.status = 'on'
            image_path = '/home/pi/temp/image_1.jpg'
            logger.info('start_yolo')
            self.detections = detect_objects_with_custom_model(image_path, self.model_path)
            logger.info('finish_yolo')

            if self.detections:
                self.largest_detections = max(self.detections, key=lambda x: x['area_box'])
                if self.largest_detections['center_normalized_y'] < 0.7:
                    self.status = 'on'
                    logger.info(self.largest_detections['label'])
                    self.label = self.largest_detections['label']
                    print('Yolo: ',self.largest_detections['center_normalized_x'], ',', self.largest_detections['center_normalized_y'])
                    return self.largest_detections['center_normalized_x'], self.largest_detections['center_normalized_y'], self.label, self.status
                if self.largest_detections['center_normalized_y'] >= 0.7:
                    self.status = 'finish'
                    #logger.info(self.largest_detections['label'])
                    self.label = self.largest_detections['label']
                    print('Yolo: ',self.largest_detections['center_normalized_x'], ',', self.largest_detections['center_normalized_y'])
                    return None, None, self.label, self.status
            else:
                self.status = 'on'
                return None, None, None, self.status
            
        return None, None, self.label, self.status

    
