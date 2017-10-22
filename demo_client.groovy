#!/usr/bin/env groovy
@Grapes(
    @Grab(group='org.neo4j.driver', module='neo4j-java-driver', version='1.4.4')
)

import org.neo4j.driver.v1.*

def cli = new CliBuilder(usage: 'Fire continously cypher queries')
cli.with {
	h longOpt: 'help', 'show usage information'
    w longOpt: 'write', "apply the cypher command in a 'write' transaction"
    u longOpt: 'url', args: 1, "bolt connect string"
    c longOpt: 'cypher', args:1, "cypher command"
    s longOpt: 'sleep', args:1, 'sleeping time in secs'

}
def options = cli.parse(args)
if (!options) {
	return
}
if (options.h) {
	cli.usage()
	return
}

def mode = options.w ? AccessMode.WRITE : AccessMode.READ
def url = options.u ?: 'bolt+routing://192.168.178.100:7687'
def cypher = options.c ?: 'match (n) return count(*)'
int s = options.s ?: 1

println("connecting to $url every $s secs in $mode mode running $cypher")

def driver = GraphDatabase.driver(url)
println('driver initialization done.')
while (true) {

	def session 
	try {
		session = driver.session(mode)
		result = session.run(cypher).single().get(0)
		println "we have $result nodes"
	} catch (Exception e) {
		println "oops: $e.message"
	} finally {
		session.close()
	}
	sleep(s*1000)
}
