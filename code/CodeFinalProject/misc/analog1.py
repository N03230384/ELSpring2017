#!/usr/bin/python

import smbus
import time

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
avg = avg / end
print avg
