#!/home/pi/.virtualenvs/stephmeter/bin/python

import nextbus
import pwm_calibrate
import led
import time
from settings import *

def main():
	l = led.LED(SERIAL_DEVICE, SERIAL_SPEED)
	p = pwm_calibrate.PWMCalibrator(smoothing=True)
	p.load()
	p_range = p.get_range()
	nb = nextbus.NextbusPredictor(NEXTBUS_ROUTES)

	while True:
		nb.refresh_if_necessary()
		predictions = (nb.get_nth_closest_arrival(0), nb.get_nth_closest_arrival(1))
		for (route, minutes) in predictions:
			minutes = min(max(minutes, p_range[0]), p_range[1])
			if int(route)==43:
				l.set(0, 100, 0)
			elif int(route)==42:
				l.set(0, 0, 100)
			p.setPWM(minutes)
			time.sleep(3)


if __name__ == '__main__':
	main()

