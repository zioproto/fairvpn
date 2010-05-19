import os
import sys
import socket
import time

#Sequentially select a node and connect it with all other nodes in the slice

# MAIN #
f=open("nodes.txt","r")
x=f.readlines()

for node1 in x:
	for node2 in x:
		if(node1 != node2):
			cmd="ssh -n -T -l uniroma2_fairvpn "+node1[0:len(node1)-1]+" './iperf -c "+node2[0:len(node2)-1]+" -p 61600 -y C >>out.txt'"
			os.system(cmd)

			
		
	
	
