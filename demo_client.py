#!/usr/bin/env python3

from neo4j.v1 import GraphDatabase, WRITE_ACCESS, READ_ACCESS
from time import sleep
from argparse import *

parser = ArgumentParser(description='Fire continously cypher queries')

parser.add_argument("-w", "--write", help="apply the cypher command in a 'write' transaction", action="store_true", default=False)
parser.add_argument("-u", "--url", help="bolt connect string", default="bolt+routing://192.168.178.100:7687")
parser.add_argument("-c", "--cypher", help="cypher command", default="match (n) return count(*)")
parser.add_argument("-s", "--sleep", help="sleeping time in secs", default=1)
args = parser.parse_args()

#print(args)
mode = WRITE_ACCESS if args.write else READ_ACCESS 
print("connecting to %s, running '%s' every %d in %s mode" %(args.url, args.cypher, args.sleep, mode))

driver = GraphDatabase.driver(args.url)
print("driver initialization done.")

#def add_node(tx):
#    tx.run("create ()")

#def count_nodes(tx):
#    print("counting")
#    return tx.run("match (n) return count(n) as c").single()[0]

#def gpio_callback_2():
#    print "GPIO_CALLBACK write!"
#    with driver.session() as session:
#        session.write_transaction(add_node)

while True:
	try: 
		with driver.session(mode) as session:
			count = session.run(args.cypher).single()[0]
			print("we have %d nodes" % (count))
	except Exception as e:
		print(e)
	sleep(args.sleep)

