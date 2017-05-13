#! /usr/bin/env python
# python programa to comunicate with an MCP3008
# Import our SpiDe wrapper and our sleep function
import RPi.GPIO as GPIO
import spidev
from time import sleep
import os 

# Establish SPI device on Bus 0,Device 0

spi = spidev.SpiDev()
spi.open(0,0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

try: 

	def getAdc(channel):
# Preform SPI transaction and store returned bits in 'r'
     		r = spi.xfer([1, (8+channel) << 4, 0])
     		print r
#Filter data bits from retruned bits
     		adcOut = ((r[1]&3) << 8) + r[2]
     		percent = int(round(adcOut/10.24))
#print out 0-1023 value and percentage
    		print("ADC output: {0:4d} Percentage: {1:3}%".format (adcOut,percent))
     		sleep(0.1)

	while True:
     		getAdc(4)


except KeyboardInterrupt:
        os.system('clear')
        print("exiting cleanly")
        GPIO.cleanup()
