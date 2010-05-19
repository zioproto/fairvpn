import sys
import xmlrpclib

if(len(sys.argv)<4):
	print "bad command \ntype :python print_nodes.py <username> <password> <slicename>"
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

	node_ids = api_server.GetSlices(auth,slicenm, ['node_ids'])[0]['node_ids']
	f=open("./nodes.txt","w")
	for node in api_server.GetNodes(auth, node_ids, ['hostname']):
		print node['hostname']
		f.write(node['hostname']+"\n")
	f.close()





