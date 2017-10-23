#!/bin/sh

sudo iptables -A INPUT -p tcp -m multiport --dports 7687,5000,6000,7000,7474,7473 -j REJECT --reject-with tcp-reset
sudo iptables -A OUTPUT -p tcp -m multiport --dports 7687,5000,6000,7000,7474,7473 -j REJECT
