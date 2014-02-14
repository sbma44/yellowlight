#!/home/pi/.virtualenvs/stephmeter/bin/python

import nextbus
import led
import time
import datetime
import sys
import os
from settings import *
import wiringpi

DEBUG = '--debug' in map(lambda x: x.lower().strip(), sys.argv)

def on():
	if DEBUG:
		print 'ON'
	else:
        	wiringpi.digitalWrite(6, wiringpi.HIGH)

def off():
	if DEBUG:
		print 'OFF'
   	else:
    		wiringpi.digitalWrite(6, wiringpi.LOW)

def setup():
	if not DEBUG:
		wiringpi.wiringPiSetup()
	        wiringpi.pinMode(6, wiringpi.OUTPUT)	

def main():
	if DEBUG:
		print 'Entering debug mode...'

	nb = nextbus.NextbusPredictor(NEXTBUS_URLS)

	while True:
		nb.refresh_if_necessary()

		appropriate_route = None
		for route in NEXTBUS_URLS.keys():
			if datetime.datetime.now().hour in NEXTBUS_HOURS.get(route, []):
				appropriate_route = route


		if DEBUG:
			print 'found actively monitored route: %s' % appropriate_route

		if appropriate_route is None:
			continue

		predictions = (nb.get_nth_closest_arrival(n=0, route=appropriate_route),)

		if DEBUG:
			print 'predictions: %s' % str(predictions)

		light_should_be_on = False
		for pred in predictions:
			if pred is not None:
				(route, minutes) = pred
				if route=='G2':
					if (minutes>=5) and (minutes<=8):
						light_should_be_on = True
				if route=='64':
					if (minutes>=5) and (minutes<=8):
						light_should_be_on = True


		if light_should_be_on:
			on()
		else:
			off() 

		time.sleep(3)


if __name__ == '__main__':
	setup()
	off()
	main()

	#try:
	#	main()
	#except Exception, e:
	#	f = open('/var/log/stephmeter-crash.log', 'a')
	#	f.write(str(e))
	#	f.close()

	#	os.system('echo "%s" | mail -s "YELLOWLIGHT CRASH LOG" thomas.j.lee@gmail.com' % str(e))

