#!/usr/bin/python 
import os
import time
import sqlite3 as mydb 
import sys

""" Log Current Time, Temperature in Celsius and Fahrenheit 
    To an Sqlite3 database """

def readTemp():
	tempfile = open("/sys/bus/w1/devices/28-041692b69eff/w1_slave") 
	tempfile_text = tempfile.read()
	currentTime=time.strftime('%x %X %Z')
	tempfile.close() 
	tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000 
	tempF=tempC*9.0/5.0+32.0
	return [currentTime, tempC, tempF]

def logTemp():
	con = mydb.connect('/home/pi/Tests/temperature.db') 
        with con:
#looped through 20 times because we wanted 10 minutes worth of readings every 30 seconds
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
	  #sleeps for 30 seconds to make sure it waits before reading again
	  time.sleep(30)
		

logTemp()
