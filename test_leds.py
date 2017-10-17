#!/usr/bin/python

import wiringpi, atexit
from time import sleep  


GREEN = 17
YELLOW = 27
RED = 22

def led_off():
	wiringpi.digitalWrite(GREEN, 0)
	wiringpi.digitalWrite(YELLOW, 0)
	wiringpi.digitalWrite(RED, 0)

atexit.register(led_off)

# initialize
wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(GREEN, 1) 
wiringpi.pinMode(YELLOW, 1)
wiringpi.pinMode(RED, 1)

while True:
	wiringpi.digitalWrite(GREEN, 1)
	sleep(1)
	wiringpi.digitalWrite(YELLOW, 1)
	sleep(1)
	wiringpi.digitalWrite(RED, 1)
	sleep(1)
	led_off()
	sleep(1)
