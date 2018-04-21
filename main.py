import RPi.GPIO as GPIO # Raspberry GPIO module
import time
from datetime import datetime
import GPIO_CONTROL #Our module to control peripherals connected to the gpios (buttons, lcd, motor, buzzer) 
################################# Function Definitions ###########################

####################################################

#Main program
try:
    motor = GPIO_CONTROL.Motor() # start motor object with default values ( GPIO = 21 , BCM_MODE)
    
    #Main loop
    while True:
        motor.turnOn()
        print( str(datetime.now()) + " | Motor On" )  # DEBUG
        time.sleep(2)
        motor.turnOff()
        print( str(datetime.now()) + " | Motor Off" ) # DEBUG
        time.sleep(2)

except KeyboardInterrupt:
    print("\nProgram Stopped")
    import menu 
    GPIO.cleanup()

except SystemExit:
    print("System Exit")
    GPIO.cleanup()
