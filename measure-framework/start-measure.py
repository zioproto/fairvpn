import os
import sys
import socket
import random
import threading
from threading import Thread
import time

def generatepareto():
        return random.paretovariate(1.2)

def generatenumber():
        return random.random()*5


class schiavo(Thread):
	def __init__ (self,ips,ipd):
		Thread.__init__(self)
		self.ips = ips
		self.ipd = ipd
		self.status = -1
	def run(self):
		#time.sleep(2)
		self.alive = True
		while(self.alive):
			numK=int(generatepareto());
			cmd = ossh+"  -l root "+self.ips+" \"iperf -c "+self.ipd+" -n "+str(numK)+"M -y C\" >> outputmisure"
			#print cmd
			print "Start thread, source:\t" +self.ips+"\tand destination:\t"+ self.ipd+"\tBytes: "+str(numK)+"M\n"
			os.system(cmd)
			time.sleep(1)

#Start this script from the bootstrap nodes
#first parse

#MAIN#

ossh="ssh -o \"UserKnownHostsFile /dev/null\" -o \"StrictHostKeyChecking no\""

nodes_overlay = []
nodes_underlay = []
#load all nodes on a list
lista=open("/fairvpn/hosts/nodes","r")
for linea in lista.readlines():
	try:
		ipaddress = linea.split()[0]
		hostname = linea.split()[1]
		if (".public" in hostname ):
			#newhostname=hostname.split('.')[0]
			nodes_underlay.append(ipaddress)
			continue
		if ("10." in ipaddress ):
			nodes_overlay.append(ipaddress)
	except:
		continue

lista.close()

#print nodes

#example
#ossh -l root 192.168.100.186 "iperf -c 192.168.100.17 -y C" > filetest	

threads_list = []

for nodo in nodes_overlay:
	dest = random.choice(nodes_overlay)
	while (dest == nodo):
		dest = random.choice(nodes_overlay)
	current = schiavo(nodo,dest)
	threads_list.append(current)
	current.start()

print "All threads launched"

for i in range (1,120):
	print "Seconds:"+str(i)+"\n"
	time.sleep(1)


for thread in threads_list:
	thread.alive=False

print "Waiting for all threads to finish\n"

