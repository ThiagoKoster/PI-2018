import RPi.GPIO as GPIO # Raspberry GPIO module #DEBUG
from datetime import datetime,time,timedelta
from time import sleep
import sys
import asyncio 
import GPIO_CONTROL #Our module to control peripherals connected to the gpios (buttons, lcd, motor, buzzer) #DEBUG
################################# Function Definitions ###########################

#void -> list of datetime.time objects
def getSelectedTimes():

    fileLines = open('horarios.txt', 'r').read().splitlines() # put each line of the file in an list of strings
    selectedTimes = [] #list of datetime objects
    option = fileLines[0] # option is on the first line
    timesString = fileLines[1].split(" ") 

    for i in range(len(timesString)): #convert timeString on a list of datetime.datetime objects
        selectedTimes.append(datetime.strptime(timesString[i],"%H:%M")) 

    if option == '1': # option 1 - user gives the schedule
        selectedTimes = toTimeObject(selectedTimes)
    elif option == '2':# option 2 - user gives a start time and an interval and we generate a schedule based on that
        selectedTimes = generateSchedule(selectedTimes[0],selectedTimes[1]) # ( startTime , interval )
        selectedTimes = toTimeObject(selectedTimes) #we can only use timedelta arithmetic on datetime.datetime objects
        #thats why we convert it later to datetime.time
    else:
        print('ERROR : Arquivo horarios.txt está formatado incorretamente')
        sys.exit()
    return option,selectedTimes # option, selectedTImes

#converts a list of datetime.time to datetime.time objects
# list datetime.datetime objects -> list datetime.time objects
def toTimeObject(selectedTimes):
    for i in range(len(selectedTimes)):
        selectedTimes[i] = selectedTimes[i].time().replace(second=0,microsecond=0) #convert datetime to time cutting out seconds and microseconds
    return selectedTimes

#generates a schedule based on a start time and an interval
# datetime.datetime object , datetime.datetime object -> list datetime.datetime objects
def generateSchedule(startTime, interval):
    schedule = []
    endTime = startTime + timedelta(days=1)
    delta = timedelta(hours = interval.hour , minutes = interval.minute)
    while startTime < endTime:
        schedule.append(startTime)
        startTime += delta
    return schedule
    
####################################################
rotations = 3
#Main program
try:
    motor = GPIO_CONTROL.Motor() # start motor object with default values ( GPIO = 21 , BCM_MODE) #DEBUG
    option,selectedTimes = getSelectedTimes()
    loop = asyncio.get_event_loop()
    lastActiveTime = 0 # initialize lastActiveTime
    while True:
        ###### TODO  ######
        # Print Option Selected and Schedule? dont know if its really necessary
        timeNow = datetime.now().time().replace(second=0 , microsecond=0) # cut out seconds and microseconds
        print(datetime.now().time())
        for i in selectedTimes:
            if lastActiveTime == timeNow: #prevent from activating more than once on the same minute
                break             
            elif timeNow == i : 
                lastActiveTime = timeNow
                loop.run_until_complete(motor.feedPet(rotations))
                #loop.close()
        sleep(20) #lower cpu ultilization inside the while loop <- improve this
    #loop.close()
            
except KeyboardInterrupt:
    print("\nProgram Stopped")
    GPIO.cleanup() #DEBUG
    import menu

except SystemExit:
    GPIO.cleanup() #DEBUG
    print("System Exit")
