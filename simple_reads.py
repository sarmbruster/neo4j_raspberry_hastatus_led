#!/usr/bin/env python

from neo4j.v1 import GraphDatabase
from time import sleep

driver = GraphDatabase.driver("bolt+routing://192.168.178.100:7687")

print "driver init done."

def add_node(tx):
    tx.run("create ()")

def count_nodes(tx):
    print "counting"
    return tx.run("match (n) return count(n) as c").single()[0]

#def gpio_callback_2():
#    print "GPIO_CALLBACK write!"
#    with driver.session() as session:
#        session.write_transaction(add_node)

while True:
    with driver.session() as session:
        print "session"
        count = session.read_transaction(count_nodes)
        print "we have %d nodes" % (count)
        sleep(1)

