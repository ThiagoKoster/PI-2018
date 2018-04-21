import RPi.GPIO as GPIO

class Motor:

    #Initializations
    def __init__(self, pinNumber = 21, pinMode = GPIO.BCM):
        self.pinNumber = pinNumber
        self.pinMode = pinMode
        GPIO.setmode(self.pinMode())
        GPIO.setwarnings(False)
        GPIO.setup(self.pinNumber, GPIO.OUT)

    #Function to turn the motor on
    def turnOn(self):
        GPIO.output(self.pinNumber, GPIO.HIGH)

    #Function to turn the motor off
    def turnOff(self):
        GPIO.output(self.pinNumber, GPIO.LOW)

    #maybe a function to control speed  if needed?

