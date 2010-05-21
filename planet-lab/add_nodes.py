import os
import sys
import xmlrpclib

if(len(sys.argv)<4):
	print "bad command \ntype :python add_nodes.py <username> <password> <slicename>"
	sys.exit(1)
else:
	
	api_server = xmlrpclib.ServerProxy('https://www.planet-lab.eu/PLCAPI/')

	usern=sys.argv[1]
	passwd=sys.argv[2]
	slicenm=sys.argv[3]


	auth = {}
	auth['Username'] = usern
	auth['AuthString'] = passwd
	auth['AuthMethod'] = "password"
	
	#query="wget 'http://comon.cs.princeton.edu/status/tabulator.cgi?table=table_nodeviewshort&format=nameonly&persite=1&select=resptime>0' -O ./nodes.txt"
	query2="wget 'http://comon.cs.princeton.edu/status/tabulator.cgi?table=table_nodeviewshort&format=nameonly&persite=1&select=(resptime > 0 && 1minload < 2 && liveslices <= 5) && ((drift > 1m || (dns1udp > 80 && dns2udp > 80) || gbfree < 5 || sshstatus > 2h) == 0)' -O ./nodes.txt"	
	os.system(query2)
	
	node_list = [line.strip() for line in open("./nodes.txt")]

	api_server.AddSliceToNodes(auth,slicenm, node_list[0:100])

	print "Added nodes"
