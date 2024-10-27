class Car_select:
    def __init__(self):
        self.i = 0

    def run(self,total_status, rtn_steering,rtn_throttle,cv2_steering,cv2_throttle,yolo_steering,yolo_throttle):
        print("total:",total_status)
        match total_status:
            case 'rtn':
                #print('rtn_steering, rtn_throttle(car_select):', rtn_steering, ',', rtn_throttle)
                return rtn_steering,rtn_throttle
            case 'yolo':
                return yolo_steering,yolo_throttle
            case 'cv2': 
                return cv2_steering,cv2_throttle

class Status_Control:
    def __init__(self):
        self.rtn_status = 'stay'
        self.yo_status = 'stay'
        self.cv2_status = 'stay'


    def run(self, rtn_status, yo_status, cv2_status):
    # keep looping infinitely until the thread is stopped
        self.rtn_status = rtn_status
        self.yo_status = yo_status
        self.cv2_status = cv2_status

        print("rtn:",self.rtn_status)
        print("yolo:",self.yo_status)
        print("cv2:",self.cv2_status)

        if self.rtn_status == 'stay':
            return 'rtn'
        if self.rtn_status == 'on':
            return 'rtn'

        if self.yo_status == 'stay':
            return 'yolo'
        if self.yo_status == 'on':
            return 'yolo'

        if self.cv2_status == 'stay':
            return 'cv2'
        if self.cv2_status == 'on':
            return 'cv2'