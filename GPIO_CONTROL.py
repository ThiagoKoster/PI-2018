import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import asyncio
import smbus

class Motor():
    
    #Initializations
    def __init__(self,motorRPM = 3, pinNumber = 21, pinMode = GPIO.BCM):
        self.pinNumber = pinNumber
        self.pinMode = pinMode
        self.motorRPM = motorRPM
        GPIO.setmode(self.pinMode)
        GPIO.setwarnings(False)
        GPIO.setup(self.pinNumber, GPIO.OUT)

    #Function to turn the motor on
    def turnOn(self):
        GPIO.output(self.pinNumber, GPIO.HIGH)

    #Function to turn the motor off
    def turnOff(self):
        GPIO.output(self.pinNumber, GPIO.LOW)

    async def feedPet(self, rotations):
    #time of motor operation
        time = 60 * rotations / self.motorRPM  
        self.turnOn()
        print( str(datetime.now()) + " | Motor On" )  
        sleep(time)
        self.turnOff()
        print( str(datetime.now()) + " | Motor Off" )

class PushButton():
    #Initializations
    def __init__(self,pinNumber):
        self.pinNumber = pinNumber
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinNumber, GPIO.IN, pull_up_down = GPIO.PUD_UP) #pull up resistor
        
        GPIO.add_event_detect(self.pinNumber, GPIO.FALLING) # detects on falling edge
                   
    # read input and return true if button was pushed, simple debounce implemented              
    def wasPushed(self):
        
        if GPIO.event_detected(self.pinNumber):
            sleep(0.025) # debounce for 25mSec
            if GPIO.input(self.pinNumber) == 0:
                return True
            else:
                return False


    
class i2c_device:
   def __init__(self, addr, port=1):
      self.addr = addr
      self.bus = smbus.SMBus(port)

# Write a single command
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)

# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)

# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class Lcd:
   #initializes objects and lcd
   def __init__(self,i2cAddress = 0x27):
      self.address = i2c_device(i2cAddress)

      self.write(0x03)
      self.write(0x03)
      self.write(0x03)
      self.write(0x02)

      self.write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.write(LCD_CLEARDISPLAY)
      self.write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)

   # clocks EN to latch command
   def strobe(self, data):
      self.address.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.address.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)

   def writeFourBits(self, data):
      self.address.write_cmd(data | LCD_BACKLIGHT)
      self.strobe(data)

   # write a command to lcd
   def write(self, cmd, mode=0):
      self.writeFourBits(mode | (cmd & 0xF0))
      self.writeFourBits(mode | ((cmd << 4) & 0xF0))

   # write a character to lcd
   def writeChar(self, charvalue, mode=1):
      self.writeFourBits(mode | (charvalue & 0xF0))
      self.writeFourBits(mode | ((charvalue << 4) & 0xF0))

   # write string function with optional char positioning
   def writeString(self, string, line=1, pos=0): #( pos = 0 to 15)
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    
    self.write(0x80 + pos_new)
    
    for char in string:
      self.write(ord(char), Rs)

   # clear lcd and set to home
   def clear(self):
      self.write(LCD_CLEARDISPLAY)
      self.write(LCD_RETURNHOME)

   # define backlight on/off (on = .backlight(1); off= .backlight(0)
   def backlight(self, state): # state 1 = on, 0 = off
      if state == 1:
         self.address.write_cmd(LCD_BACKLIGHT)
      elif state == 0:
         self.address.write_cmd(LCD_NOBACKLIGHT)

   # add custom characters (0 - 7)
   def loadCustomChars(self, fontdata):
      self.write(0x40)
      for char in fontdata:
         for line in char:
            self.writeChar(line)

   def clearLine(self,line):
      self.writeString("                  ",line)

   def clearChar(self,line,pos=0):
      self.writeString(" ",line,pos);
