#! /usr/bin/env python
import os
import re
import networkx as nx
import math as math

# Authors: Saverio Proto
# This software is released under GPL3
# Copyright Ninux.org 2010

#This script reads the the txt file from olsrd_txtinfo plug-in and ...
#Needs wget packages

bootstrap = "127.0.0.1"

fanout = 3

########################### IMPLEMENTATION #############################

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

#download topology
#os.system(" wget http://"+bootstrap+":2006 -q -O topology.txt")

#open file
topology_file=open("topology.txt",'r')
parsing=False

nodedb = set()
links = {}
apl = {}

for line in topology_file.readlines():
	if parsing:
		if line.isspace():
			parsing=False
			print "List of collected nodes:"
			for node in nodedb:
				print node
			print "list of collected links:"
			for link,etx in links.iteritems():
				uno,due=link
				print uno + "\t" + due + "\t",etx
			print "Collected ",len(nodedb), "Nodes and ",len(links),"links\n"

			G=nx.Graph()
			G.add_edges_from(links)

			#Calculate Betweenness Centrality
			bcdict = nx.betweenness_centrality(G, normalized=False, weighted_edges=False)
			for el1,el2 in bcdict.iteritems():
				print "NODE: ",el1, "\t" + "BC",el2
			
			#Calculate NC
			ncdict = bcdict.copy()
			for el1 in ncdict.keys():
				ncdict[el1]=ncdict[el1]+(len(ncdict)-1)
				print "NODE: ",el1, "\t" + "NC",ncdict[el1]
			
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

			alpha = float( 1.0 / (1-jain_index(ncdict.values())))
			print "ALPHA",alpha

			#Select FANOUT nodes to connect to
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
						print "OTHER NODES",costdict
						#update mypl
						for i in mypl.iterkeys():
							mypl[i]=min(mypl[i],fwdict[0][k][i]+1)
						print "MY CURRENT ROUTING TABLE",mypl
						
						pldict[k] = 10000
						for i in pldict.iterkeys():
							if (pldict[i] != 10000):
								pldict[i]=0 
						break
						
				






					

			
			print "stop\n\n\n\n"
			
			#for el1,el2 in fwdict[1].iteritems():
			#	print "NODE: ",el1, "\t" + "BC",el2
			break
		endpoint1=line.split()[0] #IP address of endpoint1
		endpoint2=line.split()[1] #IP address of endpoint2
		
		try:
			etx=float(line.split()[4])
		except:
			etx = 999999
		
		if endpoint1 not in nodedb:
                                nodedb.add(endpoint1) 
		if endpoint2 not in nodedb:
                                nodedb.add(endpoint2) 
		if (endpoint1,endpoint2) not in links:
				links[(endpoint1,endpoint2)] = etx
	
		#print "searching ip: %s and the other ip %s and cost %s" % (endpoint1,endpoint2,etx) 	
				
	if line.find('Dest. IP') != -1:
		parsing=True	

