import os
import sys
import socket
import random
import time

def generatepareto():
	return random.paretovariate(1.2)

def generatenumber():
	return random.random()*5

#MAIN #



while(1):
	#open file with list of nodes of the slice
	f=open("nodes.txt","r")
	x=f.readlines()
	
	#choose a two casual nodes
	casual=int(random.randrange(0,len(x)-1))
	f.close()
	node1=x[casual]

	casual=int(random.randrange(0,len(x)-1))
	print "NODO 1 :",node1
	
	while(x[casual] == node1):
		casual=int(random.randrange(0,len(x)-1))

	node2=x[casual]

	print "NODO 2 :",node2

	#Generate a casual number of bytes	
	numK=int(generatepareto());

	cmd="ssh -n -T -l uniroma2_fairvpn "+node1[0:len(node1)-1]+" './iperf -c "+node2[0:len(node2)-1]+" -p 61600 -n "+str(numK)+"M -y C >>out-random.txt'"
	print "sending "+str(numK)+"Mbyte"
	os.system(cmd)
	backofftime=generatenumber()*60
	print "In ",str(int(backofftime)),"seconds the backoff time expires"
	time.sleep(int(backofftime))

