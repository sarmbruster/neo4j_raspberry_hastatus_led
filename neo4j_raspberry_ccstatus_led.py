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
        #r = requests.get("http://localhost:7474/db/manage/server/core/writable", auth=('neo4j', '123'), timeout=0.1)
        r = requests.get("http://localhost:7474/db/manage/server/core/writable", timeout=0.1)

        if r.text == "true":
            wiringpi.digitalWrite(GREEN, 1)
            wiringpi.digitalWrite(YELLOW, 0)
            wiringpi.digitalWrite(RED, 0)

        else:
            r = requests.get("http://localhost:7474/db/manage/server/core/read-only", timeout=0.1)
            if r.text == "true":
                wiringpi.digitalWrite(GREEN, 0)
                wiringpi.digitalWrite(YELLOW, 1)
                wiringpi.digitalWrite(RED, 0)

            else:
                r = requests.get("http://localhost:7474/db/manage/server/read-replica/available", timeout=0.1)
                if r.text == "true":
                    wiringpi.digitalWrite(GREEN, 0)
                    wiringpi.digitalWrite(YELLOW, 0)
                    wiringpi.digitalWrite(RED, 1)

        sleep(1)

    except requests.exceptions.ConnectionError:
        wiringpi.digitalWrite(GREEN, 0)
        wiringpi.digitalWrite(YELLOW, 0)
        wiringpi.digitalWrite(RED, 1)
        sleep(0.5)
        wiringpi.digitalWrite(GREEN, 1)
        wiringpi.digitalWrite(YELLOW, 0)
        wiringpi.digitalWrite(RED, 0)
        sleep(0.5)

    except requests.exceptions.ReadTimeout:
        wiringpi.digitalWrite(GREEN, 1)
        wiringpi.digitalWrite(YELLOW, 1)
        wiringpi.digitalWrite(RED, 1)
        sleep(0.5)
        wiringpi.digitalWrite(GREEN, 0)
        wiringpi.digitalWrite(YELLOW, 0)
        wiringpi.digitalWrite(RED, 0)
        sleep(0.5)

