import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import asyncio
class Motor():
    
    #Initializations
    def __init__(self,motorRPM = 3, pinNumber = 21, pinMode = GPIO.BCM):
        self.pinNumber = pinNumber
        self.pinMode = pinMode
        self.motorRPM = motorRPM
        GPIO.setmode(self.pinMode)
        GPIO.setwarnings(False)
        GPIO.setup(self.pinNumber, GPIO.OUT)

    #Function to turn the motor on
    def turnOn(self):
        GPIO.output(self.pinNumber, GPIO.HIGH)

    #Function to turn the motor off
    def turnOff(self):
        GPIO.output(self.pinNumber, GPIO.LOW)

    async def feedPet(self, rotations):
    #time of motor operation
        time = 60 * rotations / self.motorRPM  
        self.turnOn()
        print( str(datetime.now()) + " | Motor On" )  
        sleep(time)
        self.turnOff()
        print( str(datetime.now()) + " | Motor Off" )

    
    
    #maybe a function to control speed  if needed?

