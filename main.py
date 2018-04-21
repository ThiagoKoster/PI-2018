import RPi.GPIO as GPIO # Raspberry GPIO module
import time
from datetime import datetime
import SDL_DS3231.SDL_DS3231 as RTC #RTC module
from GPIO_CONTROL import Motor #Our module to control peripherals connected to the gpios (buttons, lcd, motor, buzzer) 
################################# Function Definitions ###########################

####################################################

#Main program
try:
    motor = Motor()
    ds3231 = RTC()
    ds3231.write_now()
    print 
    #Main loop
    while True:
        print ("DS3231=\t\t%s") % ds3231.read_datetime()
        motor.turnOn()
        print( datetime.now() + " | Motor On" )  # DEBUG
        time.sleep(2)
        motor.turnOff()
        print( datetime.now() + " | Motor Off" ) # DEBUG
        time.sleep(2)

except KeyboardInterrupt:
    print("Program Stopped")
    GPIO.cleanup()

except SystemExit:
    print("System Exit")
    GPIO.cleanup()
