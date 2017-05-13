#!/usr/bin/python

# Start by importing the libraries we want to use

import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import time # This is the time library, we need this so we can use the sleep function
import os

GPIO.setmode(GPIO.BCM)

channel = 17

GPIO.setup(channel, GPIO.IN)

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

try:
	print("Starting Soil Humidity Sensor")
	time.sleep(3)
	os.system('clear')
	print("Ready")

	while True:
		if GPIO.input(channel) == GPIO.HIGH:
			print("motor on")
			time.sleep(1)
		
		else: 
			print("motor off")
			time.sleep(1)

except KeyboardInterrupt:
	os.system('clear')
	print("exiting cleanly")
	GPIO.cleanup()
