# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
import time
import sqlite3 as mydb
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import smbus

tempPin = 4
#moisturePin = 17
humidityPin = 22
motorPin = 27
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(tempPin, GPIO.IN)
#GPIO.setup(moisturePin, GPIO.IN)
GPIO.setup(humidityPin, GPIO.IN)
GPIO.setup(motorPin, GPIO.OUT)

        
def readTemp():
        print 'reach readTemp'
        tempfile = open("/sys/bus/w1/devices/28-041692b69eff/w1_slave")
        tempfile_text = tempfile.read()
        currentTime=time.strftime('%x %X %Z')
        tempfile.close()
        tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
        tempF=tempC*9.0/5.0+32.0
        return [currentTime, tempF]

def readHumidity():
# Parse command line parameters.
        print 'reach readHumidity'
    # 	sensor_args = { '11': Adafruit_DHT.DHT11,
   #             '22': Adafruit_DHT.DHT22,
  #              '2302': Adafruit_DHT.AM2302 }
 #	if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    	    #	sensor = sensor_args[sys.argv[1]]
                #sensor = sensor_args['22']
    	    #	pin = sys.argv[2]
               # pin = '22'
#	else:
 #   		print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
  #  		print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
#    		sys.exit(1)

	sensor = 22
	pin = 22
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
    		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
   		print('Failed to get reading. Try again!')
    		sys.exit(1)

  	return [temp, humidity]

def readMoisture(channel):
 #    if ((channel>7)or(channel<0)):
 #	return -1
    # r = spi.xfer([1, (8+channel) << 4, 0])
    # adcOut = ((r[1]&3) << 8) + r[2]
    # percent = int(round(adcOut/10.24))
        print 'reach readMoisture'
	bus = smbus.SMBus(1)
	aout = 0
	avg = 0
	end = 50
#to get an accurate reading we will average 50 reads 
	for x in range(0,end):

        	for a in range(0,4):
                	bus.write_byte_data(0x48,0x40 | ((a+1) & 0x03), 0)
                	v = bus.read_byte(0x48)
                	percent = int(round(v/10.24))
#getting value at first channel
                	if a == 0:
                        	#val = v
                        	#print percent
                        	val = percent
                        	avg = avg + val
	avg = avg/end   
	return [avg]

def startMotor(moisture_percent):
	needed_moisture = 14
	if(moisture_percent >= needed_moisture):
		GPIO.output(motorPin, 1)
		print("water pump on")
		return 1

	if(moisture_percent <= needed_moisture):
		GPIO.output(motorPin, 0)
		print("water pump off")
		return 0
       #returns 1 or 0 depending on if pump is turned on or not

def logData():
       con = mydb.connect('/home/pi/Final/projec_data.db')
       with con:   
          try:
# call temp
               [t,C,F]=readTemp()
               print "Current temperature is: %s F" %F
# call humidity
#               [h, t2] = readHumidity()
# call moisture
               [m] = readMoisture()
# call waterpump
               [w] = startMotor(m)

               cur = con.cursor()
               #sql = "insert into db"
               cur.execute('insert into Data values(?,?,?,?,?,?)', (t,F,h,t2,m,w))
               print "Everything logged"
          except:
                print "Error!!"
          #sleeps for 43200 seconds to make it read every 12 hours
       time.sleep(43200)

def main():
        #Every x amount of time call all sensors
        #log all to database
        try:
                print("test")
                logData()
        except KeyboardInterrupt:
        #        os.system('clear')
                print("exiting cleanly")
                GPIO.cleanup()
main()
