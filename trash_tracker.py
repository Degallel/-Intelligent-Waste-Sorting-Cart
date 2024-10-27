import cv2
import numpy as np
from donkeycar.parts.camera import PiCamera

#处理一个图像帧，检测图像中的橙色对象，并返回最大的对象中心的 x 坐标
def process_frame(frame):
    # Convert from RGB to HSV for better color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Define the color range for the ping-pong ball and apply the mask
    lower_orange = np.array([0, 120, 120])
    upper_orange = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour and get its center
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)

        if moments["m00"] != 0:
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
            return cX, cY
    return None, None


class cv2_get:
    def __init__(self, steer=390, turn_gain=0.5):
        self.steer = steer
        self.turn_gain = turn_gain
        self.cX = 0
        self.cY = 0

    '''
    def get_control(self, pingpong_x, frame_width):
        if pingpong_x is None:
            return 0.0, 0.0  # You may want to stop the car if the ball is not detected

        error = frame_width / 2 - pingpong_x
        angle = error * self.turn_gain
        return self.throttle, angle
    '''
    
    def run(self,img):
        self.cX, self.cY = process_frame(img)
        #print(self.cX, self.cY)
        return self.cX, self.cY
    

class carCol:
    def __init__(self, turn_gain=1, throttle_gain=1):
        self.turn_gain = turn_gain
        self.throttle_gain = throttle_gain
        self.cX = 0
        self.cY = 0

    '''
    def get_control(self, pingpong_x, frame_width):
        if pingpong_x is None:
            return 0.0, 0.0  # You may want to stop the car if the ball is not detected

        error = frame_width / 2 - pingpong_x
        angle = error * self.turn_gain
        return self.throttle, angle
    '''
    
    def run(self, cX, cY):
        self.cX = cX
        self.cY = cY
        print("(X,Y):(",self.cX, self.cY, ')')
        if self.cX != None and self.cY != None:
            steering =  self.turn_gain*(self.cX - 180) / 180
            throttling = self.throttle_gain*( 200 - self.cY) / 200
            
            print("steer,thro:", steering,throttling)
            print('\n')

            return steering, throttling
        print("bb.kk.bbk")
        return 0, 0
        