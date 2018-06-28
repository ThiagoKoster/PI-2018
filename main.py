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

#############################################################
###########################################################
############# MENU
def getMenuOptions():
    lcd.clear()
    lcd.writeString("> Opcao 1",1,0)
    lcd.writeString("  Opcao 2",2,0)
    option = 1
    while not confirmButton.wasPushed():
        if upButton.wasPushed():
            option = 1
            lcd.clearChar(2,0)
            lcd.writeString(">",1,0)
        elif downButton.wasPushed():
            option = 2
            lcd.clearChar(1,0)
            lcd.writeString(">",2,0)
    return option


def getTime(textToPrint,inputTime):
    
    hourDelta = timedelta(hours=1)
    minuteDelta = timedelta(minutes = 1)
    lcd.clear()
    lcd.writeString(textToPrint)
    lcd.writeString( inputTime.strftime('%H:%M'),2,5)
    while(not confirmButton.wasPushed()): #hour digit
        lcd.writeString("*",2,4)
        if upButton.wasPushed():
            inputTime += hourDelta
            lcd.clearLine(2)
            lcd.writeString( inputTime.strftime('%H:%M'),2,5)
        elif downButton.wasPushed():
            inputTime -= hourDelta
            lcd.clearLine(2)
            lcd.writeString( inputTime.strftime('%H:%M'),2,5)
    while(not confirmButton.wasPushed()):  #minute digit
        lcd.writeString(" ",2,4)
        lcd.writeString("*",2,10)
        if upButton.wasPushed():
            inputTime += minuteDelta
            lcd.clearLine(2)
            lcd.writeString( inputTime.strftime('%H:%M'),2,5)
        elif downButton.wasPushed():
            inputTime -= minuteDelta
            lcd.clearLine(2)
            lcd.writeString( inputTime.strftime('%H:%M'),2,5)
    return inputTime.strftime('%H:%M')


def getNumber(textToPrint):
    timesNumber = 1
    lcd.clear()
    lcd.writeString(textToPrint)
    
    while(not confirmButton.wasPushed()):
        if(downButton.wasPushed() and timesNumber > 1):
            timesNumber -= 1
            lcd.clearLine(2)
        elif (upButton.wasPushed() and timesNumber < 3):
            timesNumber += 1
            lcd.clearLine(2)

        lcd.writeString(str(timesNumber),2,7)
    
    return timesNumber
        


def schedule(option):
    inputTime = datetime.now().replace(minute=00)
    if option == 1:
        userTimes = ""
        timesNumber = getNumber("Num. de horarios")
        for index in range(0,timesNumber):
            if(index == timesNumber-1):
                userTimes += getTime("Horario " + str(index + 1),inputTime)
            else:
                userTimes += getTime("Horario " + str(index + 1), inputTime) + " "



    elif option == 2:
        startTime = getTime("Horario Inicial",inputTime)
        interval  = getTime("   Intervalo",inputTime.replace(hour=0))
        userTimes = startTime + " " + interval

    file = open("horarios.txt", "w")
    file.write(str(option) +"\n")
    file.write(userTimes)
    file.close()

#################################################### END OF MENU FUNCS

# Interface objects
upButton = GPIO_CONTROL.PushButton(20)
downButton = GPIO_CONTROL.PushButton(16)
confirmButton = GPIO_CONTROL.PushButton(26)
lcd = GPIO_CONTROL.Lcd()

#inits
lcd.clear()
rotations = 0.5

#Main program
try:
    while True:
        #### menu #####
        option = getMenuOptions()
        schedule(option)
        #### menu end #####

        mainLoop = True
        lcd.clear()
        lcd.writeString("Iniciando...")
        sleep(1)
        motor = GPIO_CONTROL.Motor() # start motor object with default values ( GPIO = 21 , BCM_MODE) #DEBUG
        option,selectedTimes = getSelectedTimes()
        loop = asyncio.get_event_loop()
        lastActiveTime = 0 # initialize lastActiveTime
        oldClock = datetime.now().replace(year=1990,minute=0)

        while mainLoop:
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
                mainLoop = False


except KeyboardInterrupt:
    GPIO.cleanup() #DEBUG
    print("\nProgram Stopped\n")

except SystemExit:
    GPIO.cleanup() #DEBUG
    print("System Exit\n")
