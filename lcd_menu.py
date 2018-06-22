import RPi.GPIO as GPIO # Raspberry GPIO module #DEBUG
import GPIO_CONTROL #Our module to control peripherals connected to the gpios (buttons, lcd, motor, buzzer) #DEBUG
from datetime import datetime,time,timedelta
from time import sleep

# blue = up / red = down / green = confirm
upButton = GPIO_CONTROL.PushButton(20)
downButton = GPIO_CONTROL.PushButton(16)
confirmButton = GPIO_CONTROL.PushButton(26)
lcd = GPIO_CONTROL.Lcd()

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
    while(not confirmButton.wasPushed()):
        if upButton.wasPushed():
            inputTime += hourDelta
            lcd.clearLine(2)
            lcd.writeString( inputTime.strftime('%H:%M'),2,5)
        elif downButton.wasPushed():
            inputTime -= hourDelta
            lcd.clearLine(2)
            lcd.writeString( inputTime.strftime('%H:%M'),2,5)
    while(not confirmButton.wasPushed()):
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

option = getMenuOptions()
schedule(option)

GPIO.cleanup()
import main