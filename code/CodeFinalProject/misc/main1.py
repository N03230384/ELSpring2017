import os
import time
import sqlite3 as mydb
import sys
import Adafruit_DHT
Import RPi.GPIO as GPIO

tempPin = 4
moisturePin = 17
humidityPin = 3
motorPin = 23

GPIO.setup(tempPin, GPIO.IN)
GPIO.setup(moisturePin, GPIO.IN)
GPIO.setup(humidityPin, GPIO.IN)
GPIO.setup(motorPin, GPIO.OUT, initial = 0)

def main():
        #Every x amount of time call all sensors
        #log all to database
        logData()

def readTemp():
        tempfile = open("/sys/bus/w1/devices/28-041692b69eff/w1_slave")
        tempfile_text = tempfile.read()
        currentTime=time.strftime('%x %X %Z')
        tempfile.close()
        tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
        tempF=tempC*9.0/5.0+32.0
        return [currentTime, tempF]
def readHumidity():
# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)

  return [ temp, humidity]

def readMoisture(channel):
     if (channel>7)or(channel<0)):
	return -1
     r = spi.xfer([1, (8+channel) << 4, 0])
     adcOut = ((r[1]&3) << 8) + r[2]
     percent = int(round(adcOut/10.24))
     return [percent]

def startMotor():
Global needed_moisture
Global moisture_%=50

if(needed_moisture <= moisture_%):
	GPIO.output (motorPin,1)
	Print (“Water Pump On”)
	return 1

if(needed_moisture >= moisture_%):
	GPIO.output(motorPin,0)
	Print(“Water Pump Off”)
	return 0
#Sleep(100)

#startMotor():
       #returns 1 or 0 depending on if pump is turned on or not
def logData():
        con = mydb.connect('/home/pi/Final/projec_data.db')
       with con:   
          Try:
# call temp
               [t,C,F]=readTemp()
               print "Current temperature is: %s F" %F
# call humidity
               [h, t2] = readHumidity()
# call moisture
               spi = spidev.SpiDev()
               spi.open(0,0)
               [m] = readMoisture(0)
# call waterpump
               [w] = startMotor()

               cur = con.cursor()
               #sql = "insert into db"
               cur.execute('insert into plantData values(?,?,?,?,?,?)', (t,C,F,h,t2,m,w))
               print "Everything logged"
 except:
                print "Error!!"
          #sleeps for 43200 seconds to make it read every 12 hours
          time.sleep(43200)

