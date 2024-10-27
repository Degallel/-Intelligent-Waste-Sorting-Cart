from ultralytics import YOLO
model_path = '/home/pi/Downloads/best.pt'
image_path = '/home/pi/Downloads/test1.jpg'
model= YOLO(model_path)
results=model(image_path)
	
results[0].show()
	

