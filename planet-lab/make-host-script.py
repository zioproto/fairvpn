import os
import sys
import socket
#this script make the host script for tincd

#MAIN#
if( len(sys.argv)<2):
	print "bad command: type python %s <list_of_nodes_in_use>" % sys.argv[0]
	sys.exit(1);
else:
	lista=open(sys.argv[1],"r")
	for linea in lista.readlines():
		# Host-down Script
		nomefile="./hosts/"+linea.strip()+"-down"
		print nomefile
		f=open(nomefile,"w")
		f.write("#!/usr/bin/python \npython recover.py "+linea.strip()+" ../"+sys.argv[1]);
		f.close()

		# Host script
		pathf="./hosts/"+linea.strip();
                newf=open(pathf,"w")
                xx="Address = "+socket.gethostbyname(linea.strip())
                newf.write(xx);
                newf.close()

	lista.close()

		


