#!/usr/bin/python
import os
import time
import sqlite3 as mydb
import sys

""" Log Current Time, Temperature in Celsius and Fahrenheit
 To an Sqlite3 database """

def readTemp():
	tempfile = open("/sys/bus/w1/devices/28-0516921f23ff/w1_slave")
 	tempfile_text = tempfile.read()
 	currentTime=time.strftime('%x %X %Z')
 	tempfile.close()
 	tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
 	tempF=tempC*9.0/5.0+32.0
 	return [currentTime, tempC, tempF]

# In this section of the code, I placed a for loop so that the commands given
# will allow the loop to recycle itself 20 times every 30 seconds. This makes
# the loop execute for 10 total minutes while collecting the tempertaute
# data every 30 seconds.

def logTemp():
	con = mydb.connect('/home/pi/Tests/temperature.db')
	with con:
         for i in range(0,20):
 		try:
 			[t,C,F]=readTemp()
 			print "Current temperature is: %s F" %F
 			cur = con.cursor()
 			#sql = "insert into TempData values(?,?,?)"
 			cur.execute('insert into TempData values(?,?,?)', (t,C,F))
 			print "Temperature logged"
 		except:
 			print "Error!!"
                time.sleep(30)

logTemp()

