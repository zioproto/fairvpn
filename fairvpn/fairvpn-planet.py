#! /usr/bin/env python
import os
import sys
import re
import networkx as nx
import pygraphviz as pgv
import math as math
import socket
import random
import string
from socket import gethostname;
import time

# Authors: Saverio Proto
# This software is released under GPL3
# Copyright Ninux.org 2010


#Configuration
from config import *

########################### IMPLEMENTATION #############################



def fixnameandkey():
	#run after tinconfheader
	os.system(tinc_cmd+""" --config=./ -K<<EOF


	EOF""")

def tincup():
	os.system("rm tinc-up")
	os.system("echo \"ip link set dev tap0 up && ip a a dev tap0 "+myOverlayIP+"/8 broadcast 10.255.255.255\" > tinc-up")
	os.system("chmod +x tinc-up")

def tincconfheader():
	os.system("rm tinc.conf")
	os.system("rm -rf hosts")
	os.system("mkdir hosts")
	os.system("echo \"Mode = switch\" > tinc.conf")
	os.system("echo \"Name ="+gethostname().replace('-','')+"\" >> tinc.conf") 
	os.system("echo \"TunnelServer = yes\" >> tinc.conf")
	os.system("mkdir -p /usr/local/var/run/")
		  	                          
def name2ip(name):
	#ip = name.split('x')[1]+"."+name.split('x')[2]+"."+name.split('x')[3]+"."+name.split('x')[4]
	f=open("/fairvpn/hosts/nodes","r")
	listsnode=f.readlines()
	x=listsnode[6:len(listsnode)-2]
	print "the nodes are:\n"
	for lines in range(len(x)):
		indexofspace=x[lines].index('#');
		#print "la linea e': "
		l=x[lines][:indexofspace]
		#print l
		lind=l.index('\t');
		#print l[:lind]	# mi separa l indirizzo ip dal resto della stringa
		if( name == l[lind+1:len(l)]):
			return l[0:lind]		
		#print l[lind+1:] # mi separa l'ip corrispondente all ip 
#	return ip

def ip2name(ip):
	name = ip.split('.')[0]+"x"+ip.split('.')[1]+"x"+ip.split('.')[2]+"x"+ip.split('.')[3]
	return name

def overlayip2name(ip):
	f=open("./hosts/nodes","r")
	listsnode=f.readlines()
	x=listsnode[6:len(listsnode)-2]
	for lines in range(len(x)):
		indexofspace=x[lines].index('#');
		#print "la linea e': "
		l=x[lines][:indexofspace]
		#print l
		lind=l.index('\t');
		if( ip == l[0:lind]):
			print "IP : ",ip," NAME: ",l[lind+1:len(l)]
			return l[lind+1:len(l)]		
		#print l[:lind]	# mi separa l indirizzo ip dal resto della stringa
		#print l[lind+1:] # mi separa l'ip corrispondente all ip 
	#return "x"+name

def jain_index(x):
	
	k=len(x)
	sum1=0
	sum2=0
	i=0
	#sum1=math.fsum(x)
	for i in range(k):
		sum1=sum1+x[i]
		sum2=sum2+math.pow(x[i],2)
	sum1=math.pow(sum1,2)
	sum2=k*sum2
	ji = float(sum1/sum2)
	return ji

def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)


def olsr_config():

	f=open('/fairvpn/olsrd.conf','w')

	config= """
DebugLevel      0
IpVersion       4
MprCoverage   7
Hna4
{

}

IpcConnect
{

}

LinkQualityFishEye      0

LoadPlugin         "/fairvpn/lib/olsrd_dot_draw.so.0.3"
{
	PlParam     "accept" "0.0.0.0"
}

LoadPlugin "/fairvpn/lib/olsrd_httpinfo.so.0.1"
{
    PlParam     "Net"    "0.0.0.0 0.0.0.0"
}

LoadPlugin "/fairvpn/lib/olsrd_txtinfo.so.0.1"
{
    PlParam     "Accept"   "0.0.0.0"
}

LoadPlugin "/fairvpn/lib/olsrd_nameservice.so.0.3"
{
 	PlParam "name" "%s"
  	PlParam "hosts-file" "/etc/hosts"
   	PlParam "resolv-file" "/etc/resolv.conf"
	PlParam "interval" "10"
}

Interface "tap0"
{
LinkQualityMult default %.3f
}

	"""%(gethostname().replace('-','') ,(random.random()*0.05+0.95))
	 

	f.write(config)
	f.close()

	return


#MAIN

#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(('google.com', 0)) 
#myIP = s.getsockname()[0]
myOverlayIP = "10.%d.%d.%d" % (random.randint(1,254),random.randint(1,254),random.randint(1,254))
print  "MYOVERLAY IP IS ",myOverlayIP
#										da riaggiungere				#myName = ip2name(myOverlayIP)
os.system("rm /fairvpn/olsrd.conf")
olsr_config()
tincconfheader()
fixnameandkey()
tincup()

#download topology
os.system("rm topology.dot")
#os.system("wget http://"+bootstrap+"/topology.dot -O topology.dot")
os.system("/fairvpn/bin/telnet "+bootstrap+" 2004 > topology.dot")
os.system("/fairvpn/bin/rsync -av rsync://"+bootstrap+"/fairvpn hosts/")
G=nx.Graph()
if os.path.getsize("topology.dot") == 0:

	print "problem downloading topology"
	sys.exit(0)
topologyfile = open("topology.dot")

Gdot=pgv.AGraph(string.join(topologyfile.readlines()[3:],''))

print "Number of Nodes: ",Gdot.number_of_nodes()
print "Number of EDGES: ",Gdot.number_of_edges()
print "nodes ",Gdot.nodes(),"\n"
print "edges ",Gdot.edges(),"\n"

if Gdot.number_of_nodes() == 0:
	print "connect to bootstrap, no other nodes available \n"

	#os.system ("echo \"Address = "+bootstrap+"\" > hosts/"+ip2name(bootstrap))
	#print "ConnectTo = ", bootstrapName, " tinc.conf"
	os.system ("echo \"ConnectTo = "+bootstrapName+"\" >> tinc.conf ")
	os.system (tinc_cmd)
	time.sleep(5)
	os.system("/fairvpn/bin/olsrd -f /fairvpn/olsrd.conf")
	sys.exit(0)


if Gdot.number_of_nodes() <= fanout :
	#Connect to all nodes in topology
	print "Connect to all nodes"
	for ip in Gdot.nodes():
		print "provo a connettermi al nodo"
		print ip
		#os.system ("echo \"Address = "+name2ip(name)+"\" > hosts/"+name)
		os.system ("echo \"ConnectTo = "+overlayip2name(ip)+"\" >> tinc.conf ")
	os.system (tinc_cmd)
	time.sleep(5)
	os.system("/fairvpn/bin/olsrd -f /fairvpn/olsrd.conf")
	sys.exit(0)
	

#G.add_edges_from(Gdot.edges())
for edge in Gdot.edges():
	temp = (edge[0],edge[1],float(edge.attr['label']))
	G.add_weighted_edges_from([temp])

#Calculate Betweenness Centrality
bcdict = nx.betweenness_centrality(G, normalized=False, weighted_edges=True)
for el1,el2 in bcdict.iteritems():
	print "NODE: ",el1, "\t" + "BC",el2
print "\n"

#Calculate NC
ncdict = bcdict.copy()
for el1 in ncdict.keys():
	ncdict[el1]=ncdict[el1]+(len(ncdict)-1)
	print "NODE: ",el1, "\t" + "NC",ncdict[el1]
print "\n"

#Calculate F.W.
fwdict = nx.floyd_warshall(G,huge=99)
#print "FW",fwdict	

#create and init a vector with my pl to other nodes	
mypl = bcdict.copy()
for i in mypl.iterkeys():
	mypl[i]=9999		


fcdict = bcdict.copy()
for i in fcdict.iterkeys():
	fcdict[i]=0		

# Average path length that entering node would have by selecting the node #node, even considering the already selected nodes
pldict = bcdict.copy()
for i in pldict.iterkeys():
	pldict[i] = 0
try:
	alpha = float( 1.0 / (1-jain_index(ncdict.values())))
except:
	alpha = 999

print "ALPHA",alpha

#Select FANOUT nodes to connect to

ConnectToNodes = []

for i in range(fanout):
	print "Round ",i," selecting nodes\n"
	
	for node,pl_list in fwdict[0].iteritems():
		#print "Evaluating NODE: ",node#, "\t" + "Path Lengths",pl_list,"\n\n\n"
		#SUM Path len of the evaluating node, considering my already existing connections
		for ip in pl_list:
			#print "Evaluating NODE:",node, "TO NODE",ip,"MINS",pl_list[ip],mypl[ip],min(pl_list[ip],mypl[ip])
			if (pldict[node] !=10000):
				pldict[node]=pldict[node]+min(pl_list[ip]+1,mypl[ip])
				#print "pldic of ",node, "in for", pldict[node], ip
		pldict[node]=1.0*pldict[node]/len(pldict)
		#Calculate fc
		fcdict[node] = float (1/(1 + math.exp( float(-(ncdict[node]- average(ncdict.values()))/alpha) )))
		print "FC ",fcdict[node],node, "pldic ",pldict[node]
		
	#create cost dict
	costdict = pldict.copy()
	for i in costdict.iterkeys():
		costdict[i]=pldict[i]*fcdict[i]					
	for k,v in costdict.iteritems():
		if v == min(costdict.values()):
			print "selected node is ",k,"with cost ",v,"\n"
			ConnectToNodes.append(k)
			#print "OTHER NODES",costdict
			#update mypl
			for i in mypl.iterkeys():
				mypl[i]=min(mypl[i],fwdict[0][k][i]+1)
			#print "MY CURRENT ROUTING TABLE",mypl
			
			pldict[k] = 10000
			for i in pldict.iterkeys():
				if (pldict[i] != 10000):
					pldict[i]=0 
			break
			


print "Connect to selected nodes \n"
for name in ConnectToNodes:
	#os.system ("echo \"Address = "+name2ip(name)+"\" > hosts/"+name)
	os.system ("echo \"ConnectTo = "+overlayip2name(name)+"\" >> tinc.conf ")
os.system (tinc_cmd)
time.sleep(5)
os.system("/fairvpn/bin/olsrd -f /fairvpn/olsrd.conf")
sys.exit(0)
