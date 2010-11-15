import os
import sys
import socket
import random
import threading
import time


#MAIN#

ossh="ssh -o \"UserKnownHostsFile /dev/null\" -o \"StrictHostKeyChecking no\" -o \"TCPKeepAlive yes\""

nodes_overlay = []
nodes_underlay = []
#load all nodes on a list
#lista=open("/fairvpn/hosts/nodes","r")
#for linea in lista.readlines():
#	try:
#		ipaddress = linea.split()[0]
#		hostname = linea.split()[1]
#		if (".public" in hostname ):
#			#newhostname=hostname.split('.')[0]
#			nodes_underlay.append(ipaddress)
#			continue
#		if ("10." in ipaddress ):
#			nodes_overlay.append(ipaddress)
#	except:
#		continue
#
#lista.close()
#nodes_underlay.append("160.80.0.254")
for i in range(1,21):
	nodes_underlay.append("160.80.0."+str(i))

print "The command will be on "+str(len(nodes_underlay))+ " nodes\n"
print nodes_underlay
time.sleep(3)
remotecmd = sys.argv[1]
for src in nodes_underlay:
	time.sleep(60)
	cmd = ossh+" -l root "+src+" \""+remotecmd+"\""
	if (os.system(cmd) != 0):
		print "Problem!\n"
		time.sleep(1)
		


