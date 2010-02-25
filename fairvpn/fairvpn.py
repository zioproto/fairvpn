#! /usr/bin/env python
import os
import sys
import re
import networkx as nx
import pygraphviz as pgv
import math as math
import socket;

# Authors: Saverio Proto
# This software is released under GPL3
# Copyright Ninux.org 2010


#Configuration

tinc_cmd = "tincd --config=./ --bypass-security -d2 -D"
myOverlayIP = "10.0.30.214"
bootstrap = "160.80.81.106"
fanout = 3

########################### IMPLEMENTATION #############################

def fixnameandkey():
	#run after tinconfheader
	os.system("tincd --config=./ -K")

def tincup():
	os.system("rm tinc-up")
	os.system("echo \"ip link set dev tap0 up && ip a a dev tap0 "+myOverlayIP+"/24\" > tinc-up")
	os.system("chmod +x tinc-up")

def tincconfheader():
	os.system("rm tinc.conf && rm -rf hosts")
	os.system("mkdir hosts")
	os.system("echo \"Mode = switch\" > tinc.conf")
	os.system("echo \"Name ="+myName+"\" >> tinc.conf")
		  	                          
def name2ip(name):
	ip = name.split('x')[1]+"."+name.split('x')[2]+"."+name.split('x')[3]+"."+name.split('x')[4]
	return ip

def ip2name(ip):
	name = ip.split('.')[0]+"x"+ip.split('.')[1]+"x"+ip.split('.')[2]+"x"+ip.split('.')[3]
	return "x"+name

def jain_index(x):
	
	k=len(x)
	sum1=0
	sum2=0
	i=0
	sum1=math.fsum(x)
	sum1=math.pow(sum1,2)
	for i in range(k):
		sum2=sum2+math.pow(x[i],2)
	sum2=k*sum2
	ji = float(sum1/sum2)
	return ji

def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)

#MAIN

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 0)) 
myIP = s.getsockname()[0] 
myName = ip2name(myIP)

tincconfheader()
fixnameandkey()
tincup()

#download topology
os.system(" wget http://"+bootstrap+"/topology.dot -O topology.dot")

G=nx.Graph()
if os.path.getsize("topology.dot") == 0:

	print "connect to bootstrap, no other nodes available \n"

	os.system ("echo \"Address = "+bootstrap+"\" > hosts/"+ip2name(bootstrap))

	os.system ("echo \"ConnectTo = "+ip2name(bootstrap)+"\" >> tinc.conf ")
	os.system (tinc_cmd)
	sys.exit(0)
	
Gdot=pgv.AGraph("topology.dot")

print Gdot.number_of_nodes()
print "Added nodes ",Gdot.nodes(),"\n"
print "Added edges ",Gdot.edges(),"\n"

if Gdot.number_of_nodes() < fanout :
	#Connect to all nodes in topology
	print "Connect to all nodes"
	for name in Gdot.nodes():
		os.system ("echo \"Address = "+name2ip(name)+"\" > hosts/"+name)
		os.system ("echo \"ConnectTo = "+name+"\" >> tinc.conf ")
	os.system (tinc_cmd)
	sys.exit(0)
	

G.add_edges_from(Gdot.edges())

#Calculate Betweenness Centrality
bcdict = nx.betweenness_centrality(G, normalized=False, weighted_edges=False)
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
			print "MY CURRENT ROUTING TABLE",mypl
			
			pldict[k] = 10000
			for i in pldict.iterkeys():
				if (pldict[i] != 10000):
					pldict[i]=0 
			break
			


print "Connect to selected nodes \n"
for name in ConnectToNodes:
	os.system ("echo \"Address = "+name2ip(name)+"\" > hosts/"+name)
	os.system ("echo \"ConnectTo = "+name+"\" >> tinc.conf ")
os.system (tinc_cmd)
sys.exit(0)
