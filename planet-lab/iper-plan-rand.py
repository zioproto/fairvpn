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
	f=open("./codeploy/nodes.txt","r")
	x=f.readlines()
	f.seek(0,0)

	casual=int(random.randrange(0,len(x)-1))
	f.close()
	node1=x[casual]

	casual=int(random.randrange(0,len(x)-1))
	print "NODO 1 :",node1
	
	while(x[casual] == node1):
		casual=int(random.randrange(0,len(x)-1))

	node2=x[casual]


	print "NODO 2 :",node2



	
	numK=int(generatepareto());

	cmd="ssh -n -T -l uniroma2_fairvpn -i /home/claudio/.ssh/planet-lab.pub "+node1[0:len(node1)-1]+" './iperf -c "+node2[0:len(node2)-1]+" -p 61600 -n "+str(numK)+"M -y C >>out-random.txt'"
	print "invio "+str(numK)+"Mbyte"
	os.system(cmd)
	attesa=generatenumber()*60
	print "Tra ",str(int(attesa)),"secondi ripartiro"
	time.sleep(int(attesa))

