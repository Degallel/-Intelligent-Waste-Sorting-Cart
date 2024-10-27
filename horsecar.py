import cv2
import os
import time

from docopt import docopt
import numpy as np

import donkeycar as dk
from donkeycar.parts import pins
from donkeycar.parts.datastore import TubHandler
from donkeycar.parts.camera import PiCamera
from donkeycar.parts.actuator import PWMThrottle, PulseController, PWMSteering

#修改
import sys
sys.path.append(os.getcwd())
from cv2get import process_frame_blue, process_frame_red,yolo_carCol, cv2_carCol, cv2_get
from Yolo import  detect_objects_with_custom_model, yolo
from routine import Rtn
from car_select import Car_select, Status_Control
def drive(cfg):
    V = dk.vehicle.Vehicle()
    #Camera
    cam = PiCamera(image_w=360, image_h=240, image_d=3)
    cam.camera.brightness = 50
    cam.camera.contrast = 0
    cam.camera.saturation = 100
    cam.camera.sharpness = 100
    cam.camera.awb_mode = 'fluorescent'
    V.add(cam, outputs=['cam/image_array'], threaded=True)
    
    rtn = Rtn()
    V.add(rtn, inputs=['total/status'], outputs=['rtn/steering', 'rtn/throttle', 'rtn/status'])
    YoLo = yolo()
    V.add(YoLo, inputs=['total/status'],outputs=['yo/cX', 'yo/cY', 'yo/label','yo/status'])
    cXYget = cv2_get()
    V.add(cXYget, inputs=['cam/image_array', 'total/status','yo/label'],outputs=['cv2/cX', 'cv2/cY', 'cv2/status'])
    
    car_cv2_control = cv2_carCol()
    V.add(car_cv2_control, inputs=['cv2/cX','cv2/cY'],outputs=['cv2/steering','cv2/throttle'])
    car_yo_control = yolo_carCol()
    V.add(car_yo_control, inputs=['yo/cX','yo/cY'],outputs=['yo/steering','yo/throttle'])

    status_control = Status_Control()
    V.add(status_control, inputs=['rtn/status', 'yo/status', 'cv2/status'], outputs=['total/status'])

    car_select_test=Car_select() 
    V.add(car_select_test,inputs=['total/status','rtn/steering','rtn/throttle','cv2/steering','cv2/throttle','yo/steering','yo/throttle'],outputs=['steering','throttle'])

    throttle_controller = PulseController(
            pwm_pin=pins.pwm_pin_by_id("PCA9685.1:40.1"),
            pwm_scale=1.0,
            pwm_inverted=False)
    throttle = PWMThrottle(controller=throttle_controller,
                                                max_pulse=434,
                                                zero_pulse=410,
                                                min_pulse=363)
    steering_controller = PulseController(
            pwm_pin=pins.pwm_pin_by_id("PCA9685.1:40.0"),
            pwm_scale=1.0,
            pwm_inverted=False)
    steering = PWMSteering(controller=steering_controller,
                                            left_pulse=460,
                                            right_pulse=308)
    #V.add(steering, inputs=['cv2/steering'], threaded=True)
    #V.add(throttle, inputs=['cv2/throttle'], threaded=True)
    V.add(steering, inputs=['steering'], threaded=True)
    V.add(throttle, inputs=['throttle'], threaded=True)


    '''
    dt = cfg.PWM_STEERING_THROTTLE
    steering_controller = PulseController(
                pwm_pin=pins.pwm_pin_by_id(dt["PWM_STEERING_PIN"]),
                pwm_scale=dt["PWM_STEERING_SCALE"],
                pwm_inverted=dt["PWM_STEERING_INVERTED"])
    steering = PWMSteering(controller=steering_controller,
                                        left_pulse=dt["STEERING_LEFT_PWM"],
                                        right_pulse=dt["STEERING_RIGHT_PWM"])
    throttle_controller = PulseController(
                pwm_pin=pins.pwm_pin_by_id(dt["PWM_THROTTLE_PIN"]),
                pwm_scale=dt["PWM_THROTTLE_SCALE"],
                pwm_inverted=dt['PWM_THROTTLE_INVERTED'])
    throttle = PWMThrottle(controller=throttle_controller,
                                        max_pulse=dt['THROTTLE_FORWARD_PWM'],
                                        zero_pulse=dt['THROTTLE_STOPPED_PWM'],
                                        min_pulse=dt['THROTTLE_REVERSE_PWM'])
    V.add(steering, inputs=['steering'], threaded=True)
    V.add(throttle, inputs=['throttle'], threaded=True)
    '''
    V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)
    
    
if __name__ == '__main__':
    cfg = dk.load_config()
    drive(cfg)
    