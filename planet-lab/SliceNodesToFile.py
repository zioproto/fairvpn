
#TODO: da riga di comando nome slice nome utente e password

import xmlrpclib
SLICE_NAME = "uniroma2_fairvpn"
api = xmlrpclib.ServerProxy('https://www.planet-lab.eu/PLCAPI/')
auth = {'Username':"proto@ing.uniroma2.it",'AuthString':"scrivi password",'AuthMethod':'password'}
node_ids = api.GetSlices(auth, SLICE_NAME)[0]['node_ids']
#[x['hostname'] for x in api.GetNodes(auth, node_ids,['hostname'])]

file = open("nodes.txt",'w')

for x in api.GetNodes(auth, node_ids,['hostname']):
	print x['hostname']
	file.write(x['hostname']+"\n")

file.close()
