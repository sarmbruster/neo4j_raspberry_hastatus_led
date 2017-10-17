#!/usr/bin/python

import wiringpi
from time import sleep  
import requests

GREEN = 17
YELLOW = 27
RED = 22

# initialize
wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(GREEN, 1) 
wiringpi.pinMode(YELLOW, 1)
wiringpi.pinMode(RED, 1)

while True:
    try:
        r = requests.get("http://localhost:7474/db/manage/server/ha/available", auth=('neo4j', '123'), timeout=0.1)

        if r.text == "master":
            wiringpi.digitalWrite(GREEN, 1)
            wiringpi.digitalWrite(YELLOW, 0)
            wiringpi.digitalWrite(RED, 0)

        elif r.text=="slave":
            wiringpi.digitalWrite(GREEN, 0)
            wiringpi.digitalWrite(YELLOW, 1)
            wiringpi.digitalWrite(RED, 0)

    except requests.exceptions.ConnectionError:
        wiringpi.digitalWrite(GREEN, 0)
        wiringpi.digitalWrite(YELLOW, 0)
        wiringpi.digitalWrite(RED, 1)

    except requests.exceptions.ReadTimeout:
        wiringpi.digitalWrite(GREEN, 1)
        wiringpi.digitalWrite(YELLOW, 1)
        wiringpi.digitalWrite(RED, 1)

    sleep(1)
