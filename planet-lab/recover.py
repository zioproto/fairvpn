import os
import sys
import random
import socket
#this script replace a failure node with a new node

#MAIN#
if( len(sys.argv)<3):
	print "bad command: type python %s <nome_of_node> <list_of_node_in _use>" %sys.argv[0]
	sys.exit(1);
else:
	glista=open("./goodnodes.txt","r")#the list of all good nodes

	ulista=open(sys.argv[2],"r")

	good=glista.readlines()
	newnode=good[random.randrange(0,len(good)-1)]

	using=ulista.readlines()

	failnode=sys.argv[1]
	
	while newnode.strip() in using:
		newnode=good[random.randrange(0,len(good)-1)]

	print "Replacing the failure node \"%s\" with the new node \"%s\"" %(failnode,newnode)
	ulista.close()

	# update the list of node in use
	ulista=open(sys.argv[2],"w")
	try:
		using.remove(failnode+"\n")
		using.append(newnode)

		for node in using:
			ulista.write(node)
	
		glista.close()
		ulista.close()
		
		print "Creating new script for the new node"
		#make the down-script for the new node
		script=open("./hosts/"+newnode.strip()+"-down","w")
		script.write("#!/usr/bin/python \npython recover.py "+newnode.strip()+" "+sys.argv[2]);
		script.close()

		pathf="./hosts/"+newnode.strip();
                newf=open(pathf,"w")
                xx="Address = "+socket.gethostbyname(newnode.strip())
                newf.write(xx);
                newf.close()
		
		print "Removed script for the failing node"
		#remove the down-script of the node that goes down
		os.system("rm ./hosts/"+failnode+"*")

		print "launching th script on the new node"
		#Lanch the fairvon script in the new node
		command="ssh uniroma2_fairvpn@"+newnode.strip()+" \"sudo python fairvpn.py\""
		os.system(command)
	except ValueError:
		print "impossible to Recovery "
	
	
	
	
	
	
