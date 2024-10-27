from ultralytics import YOLO
from PIL import Image

# 获取图片的宽度和高度
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
                'center_normalized_y': round(center_y_norm, 4)
            })
    results[0].show() #图片显示
    return output


image_path = '/home/pi/temp/image_55.jpg'  #图片路径
model_path = '/home/pi/lulu.pt'  # YOLO 模型路径

detections = detect_objects_with_custom_model(image_path, model_path)

# 输出识别结果
for detection in detections:
    print(f"Label: {detection['label']}, Confidence: {detection['confidence']},Normalized Center: {detection['center_normalized_x']} {detection['center_normalized_y']}")
    a=detection['center_normalized_x']
    b=detection['center_normalized_y']
    print(a,b)