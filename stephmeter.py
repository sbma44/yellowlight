#!/home/pi/.virtualenvs/stephmeter/bin/python

import nextbus
import pwm_calibrate
import led
import time
from settings import *

def main():
	l = led.LED(SERIAL_DEVICE, SERIAL_SPEED)
	p = pwm_calibrate.PWMCalibrator()
	p_range = p.get_range()
	nb = nextbus.NextbusPredictor(NEXTBUS_ROUTES)

	while True:
		nb.refresh_if_necessary()
		(route, minutes) = nb.get_closest_arrival()
		minutes = min(max(minutes, p_range[0]), p_range[1])
		if int(route)==43:
			l.set(0, 255, 0)
		elif int(route)==42:
			l.set(0, 0, 255)
		P.setPWM(minutes)

		time.sleep(0.1)

if __name__ == '__main__':
	main()

