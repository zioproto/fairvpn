import os
import sys
import socket
import random
import time



# MAIN #
while(1):
	f=open("./codeploy/nodes.txt","r")
	x=f.readlines()
	casual=int(random.randrange(0,len(x)-1))
	f.close()
	node1=x[casual]
	casual=int(random.randrange(0,len(x)-1))
	print "NODO 1 :",node1
	
	while(x[casual] == node1):
		casual=int(random.randrange(0,len(x)-1))

	node2=x[casual]


	print "NODO 2 :",node2

	
	cmd="ssh -n -T -l uniroma2_fairvpn -i /home/claudio/.ssh/planet-lab.pub "+node1[0:len(node1)-1]+" './iperf -c "+node2[0:len(node2)-1]+" -p 61600 -n 1M -y C >>out.txt'"
	os.system(cmd)

	time.sleep(60)
