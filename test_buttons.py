import RPi.GPIO as GPIO
import GPIO_CONTROL
from time import sleep

# blue = up / red = down / green = confirm
blue = GPIO_CONTROL.PushButton(20)
red = GPIO_CONTROL.PushButton(16)
green = GPIO_CONTROL.PushButton(26)
lcd = GPIO_CONTROL.Lcd()

def writeCount():
    lcd.clear()
    lcd.writeString(str(count1),1,7)
    lcd.writeString(str(count2),2,7)


try:
    count1 = 0
    count2 = 0
    lcd.writeString("Starting.... ")
    sleep(1)
    selector = True
    lcd.clear()
    while True:
        if green.wasPushed():
            selector = not selector
        if selector:    
            if blue.wasPushed():
                count1 += 1
                writeCount()
            elif red.wasPushed():
                count1 -= 1
                writeCount()
        else:
            if blue.wasPushed():
                count2 += 1
                writeCount()
            elif red.wasPushed():
                count2 -= 1
                writeCount()


except KeyboardInterrupt:
    print('Exiting\n')
    GPIO.cleanup()
