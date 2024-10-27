import time
import donkeycar as dk
from docopt import docopt
from donkeycar.parts import pins
from donkeycar.parts.actuator import PWMSteering, PulseController

class sig_gen:
    def __init__(self):
        self.steering = 0.0

    def run(self):
        return self.steering

def drive():

    V = dk.vehicle.Vehicle()

    steering_controller = PulseController(
            pwm_pin=pins.pwm_pin_by_id("PCA9685.1:40.0"),
            pwm_scale=1.0,
            pwm_inverted=False)
    steering = PWMSteering(controller=steering_controller,
                                            left_pulse=460,
                                            right_pulse=320)
   
    signal_generator = sig_gen()
    V.add(signal_generator, inputs = [], outputs=['steer_io'])
    V.add(steering, inputs=['steer_io'], threaded=False)

    print("finish")
    V.start(rate_hz=20, max_loop_count=None)

    #time.sleep(2)

if __name__ == '__main__':
    #args = docopt(__doc__)
    
    #if args['drive']:
    drive()