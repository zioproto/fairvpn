#! /usr/bin/env python
import os
import re
import networkx as nx

# Authors: Saverio Proto
# This software is released under GPL3
# Copyright Ninux.org 2010

#This script reads the the txt file from olsrd_txtinfo plug-in and ...
#Needs wget packages

bootstrap = "127.0.0.1"

########################### IMPLEMENTATION #############################

#download topology
#os.system(" wget http://"+bootstrap+":2006 -q -O topology.txt")

#open file
topology_file=open("topology.txt",'r')
parsing=False

nodedb = set()
links = {}

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

			G=nx.Graph()
			G.add_edges_from(links)
			bcdict = nx.betweenness_centrality(G, normalized=False, weighted_edges=False)
			for el1,el2 in bcdict.iteritems():
				print "NODE: ",el1, "\t" + "BC",el2
			
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

