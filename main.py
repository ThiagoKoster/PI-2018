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
#Objects
lcd = GPIO_CONTROL.Lcd()
confirmButton = GPIO_CONTROL.PushButton(26)
#inits
lcd.clear()
rotations = 0.5

#Main program
try:
    lcd.clear()
    lcd.writeString("Carregando...")
    sleep(2)
    motor = GPIO_CONTROL.Motor() # start motor object with default values ( GPIO = 21 , BCM_MODE) #DEBUG
    option,selectedTimes = getSelectedTimes()
    loop = asyncio.get_event_loop()
    lastActiveTime = 0 # initialize lastActiveTime
    oldClock = datetime.now().replace(year=1990,minute=0)
    while True:
        ###### TODO  ######
        # Print Option Selected and Schedule? dont know if its really necessary
        #clock = str(datetime.now().hour) + ":" + str(datetime.now().minute)
        
        clock = datetime.now().strftime('%H:%M')
        newClock = datetime.now()
        if (newClock.minute != oldClock.minute) or (newClock.year != oldClock.year):
            lcd.clearLine(1)
            lcd.writeString(clock,1,5)
            oldClock = newClock
            print( clock )
        
        timeNow = datetime.now().time().replace(second=0 , microsecond=0) # cut out seconds and microseconds
        for i in selectedTimes:
            # TODO : mostrar prox hora de ativacao
            if lastActiveTime == timeNow: #prevent from activating more than once on the same minute
                break             
            elif timeNow == i : 
                lastActiveTime = timeNow
                loop.run_until_complete(motor.feedPet(rotations))
        if confirmButton.wasPushed() : 
            raise Exception('Call lcd_menu')
        #sleep(20) #lower cpu ultilization inside the while loop <- improve this

except Exception:
    print ("Chamando lcd_menu\n")
    GPIO.cleanup() #DEBUG
    import lcd_menu
    

except KeyboardInterrupt:
    print("\nProgram Stopped")
    GPIO.cleanup() #DEBUG
    import lcd_menu

except SystemExit:
    GPIO.cleanup() #DEBUG
    print("System Exit")
