import RPi.GPIO as GPIO # Raspberry GPIO module #DEBUG
from datetime import datetime,time
from time import sleep
import GPIO_CONTROL #Our module to control peripherals connected to the gpios (buttons, lcd, motor, buzzer) #DEBUG
################################# Function Definitions ###########################

#void -> int , array of datetime.time objects or a single datetime.time object 
def getSelectedTimes():

    fileLines = open('horarios.txt', 'r').read().splitlines() # put each line of the file in an list of strings
    selectedTimes = [] #list of datetime objects
    timesString = fileLines[1].split(" ") 
    print(timesString)
    for i in range(len(timesString)):
        selectedTimes.append(datetime.strptime(timesString[i],"%H:%M").time())
    print(selectedTimes)
    return int(fileLines[0]), selectedTimes # option, selectedTImes
    #return int(fileLines[0]), selectedTimes # selectedTimes = array of datetime.time OR a single datetime.time object 
   

####################################################

#Main program
try:
    motor = GPIO_CONTROL.Motor() # start motor object with default values ( GPIO = 21 , BCM_MODE) #DEBUG
    
    
    option,selectedTimes = getSelectedTimes()

    #Main loop for option 1
    if option == 1:
        lastActiveTime = 0 # initialize lastActiveTime
        while True:
            timeNow = datetime.now().time()
            timeNow = timeNow.replace(second=0 , microsecond=0) # cut out seconds and microseconds
            for i in selectedTimes:
                if lastActiveTime == timeNow: #prevent from activating more than once on the same minute
                        break             
                elif timeNow == i : 
                    lastActiveTime = timeNow
                    motor.turnOn() #DEBUG
                    print( str(datetime.now()) + " | Motor On" )  
                    sleep(2)
                    motor.turnOff() #DEBUG
                    print( str(datetime.now()) + " | Motor Off" ) 
                    sleep(2)
            sleep(20) #lower cpu ultilization inside the while loop <- improve this

    #Main loop for option 2
    elif option == 2: # another loop to treat option 2 ( dont know how yet) or generate the times that we want to activate based on
        while True:     # the interval given
            print('Under Construction')
            sleep(30)



except KeyboardInterrupt:
    print("\nProgram Stopped")
    GPIO.cleanup() #DEBUG
    import menu

except SystemExit:
    GPIO.cleanup() #DEBUG
    print("System Exit")
