#!/usr/bin/python

import nextbus
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

    nb = nextbus.Nextbus(NEXTBUS_URLS)

    while True:
        nb.refresh_if_necessary()

        # check if any active routes are presently monitored
        active_routes = []
        for route in NEXTBUS_URLS:
            if callable(NEXTBUS_HOURS.get(route)):
                if NEXTBUS_HOURS.get(route)():
                    active_routes.append(route)
            elif datetime.datetime.now().hour in NEXTBUS_HOURS.get(route, []):
                active_routes.append(route)

        if DEBUG and len(active_routes) > 0:
            print 'found actively monitored route(s): %s' % ', '.join(active_routes)

        if len(active_routes) == 0:
            time.sleep(60)
            continue

        prediction = nb.get_nth_closest_arrival(n=0, route=active_routes)

        if DEBUG:
            print 'predictions: %s' % str(prediction)

        light_should_be_on = False
        (route, minutes) = prediction
        if route in ('90', '92', '93'):
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