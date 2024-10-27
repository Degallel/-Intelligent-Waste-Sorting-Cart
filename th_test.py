import time
import donkeycar as dk
from docopt import docopt
from donkeycar.parts import pins
from donkeycar.parts.actuator import PWMThrottle, PulseController

class sig_gen:
    def __init__(self):
        self.throttle = -1

    def run(self):
        return self.throttle

def drive():

    V = dk.vehicle.Vehicle()

    throttle_controller = PulseController(
            pwm_pin=pins.pwm_pin_by_id("PCA9685.1:40.1"),
            pwm_scale=1.0,
            pwm_inverted=False)

    throttle = PWMThrottle(controller=throttle_controller,
                                                max_pulse=423,
                                                zero_pulse=400,
                                                min_pulse=363)
    #throttle_controller.set_pulse(380)    
    signal_generator = sig_gen()
    V.add(signal_generator, inputs = [], outputs=['throttle_io'])
    V.add(throttle, inputs=['throttle_io'], threaded=False)

    V.start(rate_hz=20, max_loop_count=None)


if __name__ == '__main__':
    drive()