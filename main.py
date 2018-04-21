import RPi.GPIO as GPIO # Raspberry GPIO module
import time
from datetime import datetime
import SDL_DS3231 #RTC module
import GPIO_CONTROL #Our module to control peripherals connected to the gpios (buttons, lcd, motor, buzzer) 
################################# Function Definitions ###########################

####################################################

#Main program
try:
    motor = GPIO_CONTROL.Motor() # start motor object with default values ( GPIO = 21 , BCM_MODE)
    ds3231 = SDL_DS3231.SDL_DS3231() # start rtc object with default values
    ds3231.write_now()
    
    #Main loop
    while True:
        print ( ("DS3231=\t\t%s") % ds3231.read_datetime())
        motor.turnOn()
        print( str(datetime.now()) + " | Motor On" )  # DEBUG
        time.sleep(2)
        motor.turnOff()
        print( str(datetime.now()) + " | Motor Off" ) # DEBUG
        time.sleep(2)

except KeyboardInterrupt:
    print("Program Stopped")
    GPIO.cleanup()

except SystemExit:
    print("System Exit")
    GPIO.cleanup()
