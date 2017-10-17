#!/usr/bin/python

import sys, re
import wiringpi
from time import sleep  

GREEN = 17
YELLOW = 27
RED = 22

wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(GREEN, 1) 
wiringpi.pinMode(YELLOW, 1) 
wiringpi.pinMode(RED, 1) 

regex = re.compile(r'^\d+.*')

while 1:
	line = sys.stdin.readline()
	if regex.search(line) is not None:
		statusGreen = wiringpi.digitalRead(GREEN)
		statusYellow = wiringpi.digitalRead(YELLOW)
		statusRed = wiringpi.digitalRead(RED)

		wiringpi.digitalWrite(GREEN, not statusGreen)
		wiringpi.digitalWrite(YELLOW, not statusYellow)
		wiringpi.digitalWrite(RED, not statusRed)
		sleep(0.2)
		wiringpi.digitalWrite(GREEN, statusGreen)
		wiringpi.digitalWrite(YELLOW, statusYellow)
		wiringpi.digitalWrite(RED, statusRed)
