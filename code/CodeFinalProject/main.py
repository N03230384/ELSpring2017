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
humidityPin = 22
motorPin = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(tempPin, GPIO.IN)
GPIO.setup(humidityPin, GPIO.IN)
GPIO.setup(motorPin, GPIO.OUT)
       
        
def readTemp():
        print 'reach readTemp'
        tempfile = open("/sys/bus/w1/devices/28-03168a2aa7ff/w1_slave")
        tempfile_text = tempfile.read()
        currentTime=time.strftime('%x %X %Z')
        tempfile.close()
        tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
        tempF=tempC*9.0/5.0+32.0
	print 'temp success'
        return [currentTime, tempF]

def readHumidity():
# Parse command line parameters.
        sensor = Adafruit_DHT.DHT22
        pin = 22
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
    		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		#air temp in F
		temperature = temperature * 1.8
		temperature = temperature + 32
	else:
   		print('Failed to get reading. Try again!')
    		sys.exit(1)

  	return [humidity,temperature]

def readMoisture():
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
	needed_moisture = 10
#needs to be >= since the higher the moisture, the lower the number in our system
	if(moisture_percent >= needed_moisture):
		GPIO.output(motorPin, True)
		print("water pump on")
		time.sleep(25)
		GPIO.output(motorPin, False)
		return "1"

	elif(moisture_percent <= needed_moisture):
		GPIO.output(motorPin, False)
		print("water pump off")
		return "0"
       #returns 1 or 0 depending on if pump is turned on or not

def logData():
       con = mydb.connect('/home/pi/Final/project_data.db')
       with con:   
          try:
# call temp
               [t,F]=readTemp()
               print "Current temperature is: %s F" %F
# call humidity
               [h, t2] = readHumidity()

               	        
# call moisture
               [m] = readMoisture()
               print "Current moisture is: %s m" %m  
# call waterpump

               [w] = startMotor(m)
               print "pumpStatus is %s "%w
	 
               cur = con.cursor()
 
               cur.execute('insert into Data values(?,?,?,?,?,?)', (t,F,h,t2,m,w))
               print "Everything logged"
          except:
                print "Error!!"
      

def main():
        #Every x amount of time call all sensors
        #log all to database
   
        try:
          while True:
                print("test")
#		GPIO.output(motorPin, False)
                logData()
#sleeps for 2 hours
                time.sleep(7200)
        except KeyboardInterrupt:
        #       os.system('clear')
                print("exiting cleanly")
                GPIO.cleanup()

main()
