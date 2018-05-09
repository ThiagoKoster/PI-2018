import RPi.GPIO as GPIO
import time
class Motor():
    motorRPM = 3
    #Initializations
    def __init__(self, pinNumber = 21, pinMode = GPIO.BCM):
        self.pinNumber = pinNumber
        self.pinMode = pinMode
        GPIO.setmode(self.pinMode)
        GPIO.setwarnings(False)
        GPIO.setup(self.pinNumber, GPIO.OUT)

    #Function to turn the motor on
    def turnOn(self):
        GPIO.output(self.pinNumber, GPIO.HIGH)

    #Function to turn the motor off
    def turnOff(self):
        GPIO.output(self.pinNumber, GPIO.LOW)



    def feedPet(rotations):
        #time of motor operation
        time = rotations/motorRPM
        turnOn()
        print( str(datetime.now()) + " | Motor On" )  
        sleep(time)
        turnOff()
        print( str(datetime.now()) + " | Motor Off" ) 


    #maybe a function to control speed  if needed?

