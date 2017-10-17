#!/usr/bin/env python
import dpkt, pcap
import re, time
import sys
import socket
import wiringpi
import threading

RED = 22

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(RED, 1)

def off():
    time.sleep(0.5)
    wiringpi.digitalWrite(RED, 0)

def __my_handler(ts,pkt):

    eth = dpkt.ethernet.Ethernet(pkt)
    ip = eth.data
    tcp = ip.data

#    fin_flag = ( tcp.flags & dpkt.tcp.TH_FIN ) != 0
    syn_flag = ( tcp.flags & dpkt.tcp.TH_SYN ) != 0
#    rst_flag = ( tcp.flags & dpkt.tcp.TH_RST ) != 0
#    psh_flag = ( tcp.flags & dpkt.tcp.TH_PUSH) != 0
#    ack_flag = ( tcp.flags & dpkt.tcp.TH_ACK ) != 0
#    urg_flag = ( tcp.flags & dpkt.tcp.TH_URG ) != 0
#    ece_flag = ( tcp.flags & dpkt.tcp.TH_ECE ) != 0
#    cwr_flag = ( tcp.flags & dpkt.tcp.TH_CWR ) != 0

    if (syn_flag == True):
        #print socket.inet_ntoa(ip.src)
        #if socket.inet_ntoa(ip.src) != "192.168.178.103":
        wiringpi.digitalWrite(RED, 1)
        threading.Thread(target=off).start()

pc = pcap.pcap(name='eth0')
pc.setfilter('tcp and dst port 7474')
#print 'listening on %s: %s' % (pc.name, pc.filter)
pc.loop(__my_handler)
