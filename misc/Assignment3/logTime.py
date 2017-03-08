#!/usr/bin/python 
import os
import time
import sqlite3 as mydb 
import sys

# This code holds the years months days, hours minutes seconds; of the 
# current date and time the information is inputed into the databse. I used the
# currentDate and currentTime to help format  the times and dates.

""" Log Current Time, Temperature in Celsius and Fahrenheit 
    To an Sqlite3 database """
def logTime():
	con = mydb.connect('/home/pi/Tests/testTime.db') 
	with con:
	  
		cur = con.cursor()
		currentDate=time.strftime('%Y-%m-%d')
		currentTime=time.strftime('%H-%M-%S')
                cur.execute('INSERT INTO timeData(xDate,xTime) values(?,?)', (currentDate,currentTime))
                con.commit()
		cur.execute("SELECT * FROM TimeData")
		print(cur.fetchall())
		print "Time logged"
logTime()
