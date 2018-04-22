import RPi.GPIO as GPIO # Raspberry GPIO module
from datetime import datetime,time
from time import sleep
import GPIO_CONTROL #Our module to control peripherals connected to the gpios (buttons, lcd, motor, buzzer) 
################################# Function Definitions ###########################
#void -> int , array of datetime.time objects or a single datetime.time object 
def getSelectedTimes():

    fileLines = open('horarios.txt', 'r').read().splitlines() # put each line of the file in an list of strings
    selectedTimes = [] #list of datetime objects

    if (fileLines[0] == '1'):  # option 1 -> various times on each line
        for i in range(1, len(fileLines)):
            # aux = (hour,minute) both are int values
            aux = list(map(int, fileLines[i].split(':')))
            # fill array with (hour,minute) datetime.time objects
            selectedTimes.append(time(aux[0], aux[1]))
    elif(fileLines[0] == '2'):  # option 2 -> base time followed by interval
        aux = list(map(int, fileLines[1].split(':'))) # aux = (hour,minute) both mapped to int values
        selectedTimes = time(aux[0], aux[1]) #base time as datetime.time object
    
    return int(fileLines[0]), selectedTimes # selectedTimes = array of datetime.time OR a single datetime.time object 
   

####################################################

#Main program
try:
    motor = GPIO_CONTROL.Motor() # start motor object with default values ( GPIO = 21 , BCM_MODE)
    
    option,selectedTimes = getSelectedTimes()

    #Main loop for option 1
    if option == 1:
        while True:
            timeNow = datetime.now().time()
            timeNow = timeNow.replace(second=0 , microsecond=0) # cut out seconds and microseconds
            lastActive = time(0,0)
            for i in selectedTimes:
                if lastActive == timeNow: # this should prevent from activating more than once
                        break             # on the same minutes but it does not, why???
                elif timeNow == i :     #maybe put line 39 here with an AND?
                    lastActive = timeNow
                    motor.turnOn()
                    print( str(datetime.now()) + " | Motor On" )  # DEBUG
                    sleep(2)
                    motor.turnOff()
                    print( str(datetime.now()) + " | Motor Off" ) # DEBUG
                    sleep(2)
            sleep(20) #lower cpu ultilization inside the while loop <- improve this

    #Main loop for option 2
    elif option == 2: # another loop to treat option 2 ( dont know how yet) or generate the times that we want to activate based on
        while True:     # the interval given
            print('Under Construction')
            sleep(30)



except KeyboardInterrupt:
    print("\nProgram Stopped")
    import menu 
    GPIO.cleanup()

except SystemExit:
    print("System Exit")
    GPIO.cleanup()
