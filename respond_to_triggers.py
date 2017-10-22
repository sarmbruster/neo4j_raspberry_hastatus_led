#!/usr/bin/env python

import os, wiringpi
from neo4j.v1 import GraphDatabase

pipe_name = '/tmp/button_to_cypher_pipe'
if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

if os.fork() == 0:  
    # listener
    pipein = open(pipe_name, 'r')
    driver = GraphDatabase.driver("bolt+routing://192.168.178.100:7687" )
    #driver = GraphDatabase.driver("bolt://192.168.178.100:7687")
    # while True:
    #     command = pipein.readline()[:-1]
    #     print("received %s." % (command))
    #     mode = WRITE_ACCESS if command=='write' else READ_ACCESS 
    #     cypher = "create ()" if command=='write' else 'match (n) return count(n) as count'

    #     with driver.session(mode) as session:
    #         print session.run(cypher).single()[0]

    while True:
        line = pipein.readline()[:-1]
        print 'Parent %d got "%s" at %s' % (os.getpid(), line, time.time( ))

else: 
    # writer
    pipeout = os.open(pipe_name, os.O_WRONLY)
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(2, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(3, wiringpi.GPIO.INPUT)
    wiringpi.pullUpDnControl(2, wiringpi.GPIO.PUD_UP)
    wiringpi.pullUpDnControl(3, wiringpi.GPIO.PUD_UP)

    wiringpi.wiringPiISR(2, wiringpi.GPIO.INT_EDGE_FALLING, lambda: os.write(pipeout, "write"))
    wiringpi.wiringPiISR(3, wiringpi.GPIO.INT_EDGE_FALLING, lambda: os.write(pipeout, "read"))
    while True:
        wiringpi.delay(2000)

# import wiringpi
# from time import sleep

# PIN_TO_SENSE = 3

# print "driver init done."

# def add_node(tx):
#     tx.run("create ()")

# def count_nodes(tx):
#     print "counting"
#     return tx.run("match (n) return count(n) as c").single()[0]


# wiringpi.wiringPiSetupGpio()
# #wiringpi.pinMode(PIN_TO_SENSE, wiringpi.GPIO.INPUT)
# wiringpi.pullUpDnControl(2, wiringpi.GPIO.PUD_UP)
# wiringpi.pullUpDnControl(3, wiringpi.GPIO.PUD_UP)


# wiringpi.wiringPiISR(2, wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_2)
# wiringpi.wiringPiISR(3, wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_3)

