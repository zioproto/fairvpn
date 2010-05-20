import os
import sys
import random
import time
import xmlrpclib

if(len(sys.argv)<5):
	print "bad command \ntype :python add_nodes.py <username> <password> <slicename> <number of node to add>"
	sys.exit(1)
else:
	
	api_server = xmlrpclib.ServerProxy('https://www.planet-lab.eu/PLCAPI/')

	usern=sys.argv[1]
	passwd=sys.argv[2]
	slicenm=sys.argv[3]
	nodenum=sys.argv[4]

	auth = {}
	auth['Username'] = usern
	auth['AuthString'] = passwd
	auth['AuthMethod'] = "password"
	
	query="wget 'http://comon.cs.princeton.edu/status/tabulator.cgi?table=table_nodeviewshort&format=nameonly&persite=1&select=resptime>0' -O ./nodes.txt"
	os.system(query)
	
	node_list = [line.strip() for line in open("./nodes.txt")]

	#select randomly the node that will be added to the slice
	node_rnd=[]
	x=int(random.randrange(0,len(node_list)))	
	node_rnd.append(node_list[x])
	count=1
	while(count<int(nodenum)):
		if(node_list[x] in node_rnd):
			x=int(random.randrange(0,len(node_list)-1))
		else:
			node_rnd.append(node_list[x])
			count=count+1			
				

	#Add to the slice the random list of nodes
	api_server.AddSliceToNodes(auth,slicenm, node_rnd)

	print "Added nodes"
