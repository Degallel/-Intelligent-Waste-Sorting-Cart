import cv2
import numpy as np


#处理一个图像帧，检测图像中的橙色对象，并返回最大的对象中心的 x 坐标
def process_frame_blue(frame):
    # Convert from RGB to HSV for better color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Define the color range for the ping-pong ball and apply the mask
    lower_orange = np.array([100, 0, 0])
    upper_orange = np.array([140, 255, 255])
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
            return cX/352, cY/240
    return None, None

def process_frame_red(frame):
    # Convert from RGB to HSV for better color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Define the color range for the ping-pong ball and apply the mask
    lower_orange = np.array([0, 0, 0])
    upper_orange = np.array([20, 255, 255])
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
            return cX/352, cY/240
    return None, None


class cv2_get:
    def __init__(self, steer=390, turn_gain=0.5):
        self.steer = steer
        self.turn_gain = turn_gain
        self.cX = 0
        self.cY = 0
        self.status = 'stay'
        self.shovel = 0
        self.unrecycling = ['paper','battle']
        self.recycling = ['bottle','can']
    
    def run(self, img, total_status,cv2_label):
        if total_status == None:
            return None, None, self.status
        
        if self.status == 'finish':
            return None, None, self.status

        if total_status == 'cv2':
            #print(cv2_label)
            
            
            if self.shovel == 0:
                import os
                import sys
                sys.path.append(os.getcwd())
                from duoji import Catch
                Catch()
                self.shovel = 1
            
            if cv2_label in self.recycling:
                self.status = 'on'
                self.cX, self.cY = process_frame_blue(img)
                #print(self.cX, self.cY)
                if self.cX != None and self.cY != None:
                    if self.cY < 0.7:
                        #self.status = 'on'
                        return self.cX, self.cY, self.status
                    if self.cY > 0.7:
                        self.status = 'finish'
                        
                        if self.shovel == 1:
                            import os
                            import sys
                            sys.path.append(os.getcwd())
                            from duoji import Catch
                            Catch()
                            self.shovel = 2
                        
                        return None, None, self.status
                else:
                    self.status = 'finish'
                    return None, None, self.status
                
            if cv2_label in self.unrecycling:
                self.status = 'on'
                self.cX, self.cY = process_frame_red(img)
                #print(self.cX, self.cY)
                if self.cX != None and self.cY != None:
                    if self.cY < 0.7:
                        #self.status = 'on'
                        return self.cX, self.cY, self.status
                    if self.cY > 0.7:
                        self.status = 'finish'
                        
                        if self.shovel == 1:
                            import os
                            import sys
                            sys.path.append(os.getcwd())
                            from duoji import Catch
                            Catch()
                            self.shovel = 2
                        
                        return None, None, self.status
                else:
                    self.status = 'finish'
                    return None, None, self.status
            
        return None, None, self.status



class yolo_carCol:
    def __init__(self, turn_gain_nearly=1.7, turn_gain_far = 1,throttle_gain=1):
        self.turn_gain_nearly = turn_gain_nearly
        self.turn_gain_far = turn_gain_far
        self.throttle_gain = throttle_gain
        self.cX = 0
        self.cY = 0

    def run(self, cX, cY):
        self.cX = cX
        self.cY = cY
        #print("carcol-(X,Y):(",self.cX, self.cY, ')')
        if self.cX != None and self.cY != None:
            if self.cY < 0.4:
                steering =  self.turn_gain_far*( self.cX - 0.5 ) / 0.5
                print("yolo_(steer,thro):", steering, 0.73)
                return steering, 0.73
                    #return steering, throttling
        
            if self.cY < 0.7 and self.cY >= 0.4:
                steering =  self.turn_gain_nearly*( self.cX - 0.5 ) / 0.5
                print("yolo_(steer,thro):", steering, 0.7)
            
                return steering, 0.73
                   #return steering, throttling
            return 0, 0
        print("yolo_no target")
        return 0, 0
        
class cv2_carCol:
    def __init__(self, turn_gain=1.1, throttle_gain=1):
        self.turn_gain = turn_gain
        self.throttle_gain = throttle_gain
        self.cX = 0
        self.cY = 0

    def run(self, cX, cY):
        self.cX = cX
        self.cY = cY
        #print("carcol-(X,Y):(",self.cX, self.cY, ')')
        if self.cX != None and self.cY != None:
            if self.cY < 0.5:
                steering =  self.turn_gain*( self.cX - 0.5 ) / 0.5
                print("cv2_(steer,thro):", steering, 0.73)
                return steering, 0.74
                   #return steering, throttling
            return 0, 0
        print("cv2_no target")
        return 0, 0