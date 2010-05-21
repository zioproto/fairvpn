import os
import sys
import xmlrpclib

if(len(sys.argv)<4):
	print "bad command \ntype :python %s <username> <password> <slicename>" % sys.argv[0]
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
	api_server.DeleteSliceFromNodes (auth, slicenm, node_ids)



