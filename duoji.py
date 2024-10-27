import RPi.GPIO as GPIO
import time

def Catch():

    GPIO.setmode(GPIO.BCM)

    # Set up the GPIO pins

    ledPin = 16

    GPIO.setup(ledPin, GPIO.OUT)

    time.sleep(1)
    GPIO.output(ledPin,GPIO.HIGH)
  
    time.sleep(2)
    GPIO.output(ledPin,GPIO.LOW)
    time.sleep(2)
    
    '''
    DS3115_pin = 12
    GPIO.setup(DS3115_pin, GPIO.OUT)
    pwm = GPIO.PWM(DS3115_pin, 50)
    pwm.start(0)


    try:
        #count = 0
        #flag = 0
        match flag:
                    case 0:
                        time.sleep(0.5)
                        pwm.ChangeDutyCycle(10)
                        time.sleep(1.5)  
                        pwm.ChangeDutyCycle(7.8)
                        time.sleep(1.5)
                    
                    case 1:
                        time.sleep(0.5)
                        pwm.ChangeDutyCycle(7.5)
                        time.sleep(1.5)
           
    except KeyboardInterrupt:
        pass
    '''
    # Clean up the GPIO pins
    GPIO.cleanup()

#Catch()