import os
import sys
import socket
import random
from threading import Thread
#import time

class schiavo(Thread):
	def __init__ (self,ips,ipd):
		Thread.__init__(self)
		self.ips = ips
		self.ipd = ipd
		self.status = -1
	def run(self):
		#time.sleep(2)
		cmd = "ossh -l root "+self.ips+" \"iperf -c "+self.ipd+" -y C\" > outputmisure"
		print cmd
		#os.system(cmd)

#Start this script from the bootstrap nodes
#first parse

#MAIN#

nodes = []

#load all nodes on a list
lista=open("/fairvpn/hosts/nodes","r")
for linea in lista.readlines():
	try:
		ipaddress = linea.split()[0]
		hostname = linea.split()[1]
		if (".public" in hostname ):
			newhostname=hostname.split('.')[0]
			nodes.append(ipaddress)
		else: 
			continue
	except:
		continue

lista.close()

print nodes

#example
#ossh -l root 192.168.100.186 "iperf -c 192.168.100.17 -y C" > filetest	

for nodo in nodes:
	#print nodo +"AND"+ random.choice(nodes)
	current = schiavo(nodo,random.choice(nodes))	
	current.start()

print "All threads launched"
