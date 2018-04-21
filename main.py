import RPi.GPIO as GPIO
import time
from datetime import datetime
################################# Function Definitions ###########################

#Function to turn the motor on
def motorOn():
    print datetime.now()
    GPIO.output(21,GPIO.HIGH)

#Function to turn the motor off
def motorOff():
    GPIO.output(21,GPIO.LOW)
####################################################


#Main program
try:
    #Initializations

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(21,GPIO.OUT)

    #Main loop
    while True:
        motorOn()
        time.sleep(2)
        motorOff()
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()

except SystemExit:
    GPIO.cleanup()
