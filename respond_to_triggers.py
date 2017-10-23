#!/usr/bin/env python

import os, wiringpi
from neo4j.v1 import GraphDatabase, WRITE_ACCESS, READ_ACCESS

pipe_name = '/tmp/button_to_cypher_pipe'
if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

pid = os.fork()
if pid == 0:  
    # listener
    pipein = open(pipe_name, 'r')
    print "%d opened named pipe %s" % (pid, pipe_name)
    driver = GraphDatabase.driver("bolt+routing://192.168.178.100:7687" )
    print "%d bolt driver initialized" % (pid)
    #driver = GraphDatabase.driver("bolt://192.168.178.100:7687")
    while True:
        command = pipein.readline()[:-1]
        print("received %s." % (command))
        mode = WRITE_ACCESS if command=='write' else READ_ACCESS 
        cypher = "create () return -1" if command=='write' else 'match (n) return count(n) as count'

        with driver.session(mode) as session:
            result = session.run(cypher).single()[0]
            print "%d, cypher result for %s is %s" % (pid, cypher, result)

else: 
    # writer
    pipeout = open(pipe_name, 'a', 0)
    print "%d opened named pipe %s for writing" % (pid, pipe_name)
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(2, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(3, wiringpi.GPIO.INPUT)
    wiringpi.pullUpDnControl(2, wiringpi.GPIO.PUD_UP)
    wiringpi.pullUpDnControl(3, wiringpi.GPIO.PUD_UP)
    print "%d GPIO configured" % (pid)

    wiringpi.wiringPiISR(2, wiringpi.GPIO.INT_EDGE_FALLING, lambda: pipeout.write("write\n"))
    wiringpi.wiringPiISR(3, wiringpi.GPIO.INT_EDGE_FALLING, lambda: pipeout.write("read\n"))
    while True:
        wiringpi.delay(2000)
