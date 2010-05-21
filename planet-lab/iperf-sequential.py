import os
import sys
import socket
import time

#Sequentially select a node and connect it with all other nodes in the slice

# MAIN #
f=open("nodes.txt","r")
x=f.readlines()
f.close()
i=0
for node1 in x:
	for node2 in x:
		if(node1 != node2):
			print "Client %s Server %s\n" % (node1,node2)
			i=i+1
			print "Round number %d" % i
			
			
			cmd_server = "ssh -n -T -l uniroma2_fairvpn "+node2[0:len(node2)-1]+" ./iperf -s -p 61600 &"
			cmd_client ="ssh -n -T -l uniroma2_fairvpn "+node1[0:len(node1)-1]+" './iperf -c "+node2[0:len(node2)-1]+" -p 61600 -y C >>out.txt'"


			cmd_killserver = "ssh -n -T -l uniroma2_fairvpn "+node2[0:len(node2)-1]+" 'killall -9 iperf'"
			cmd_killclient ="ssh -n -T -l uniroma2_fairvpn "+node1[0:len(node1)-1]+" 'killall -9 iperf'"
		
			print "killing server to make sure binding will work"
			os.system(cmd_killserver)
			time.sleep(1)
			print "starting server"
			os.system(cmd_server)
			time.sleep(1)
			print "starting client"
			os.system(cmd_client)
			time.sleep(1)
			print "killing server"
			os.system(cmd_killserver)
			time.sleep(1)
			print "killing client"
			os.system(cmd_killclient)



			
		
	
	
