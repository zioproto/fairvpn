import os
import sys
import socket
from socket import gethostbyname

def nodeonplanetlab():	
	os.system("wget \"http://comon.cs.princeton.edu/status/tabulator.cgi?table=table_nodeviewshort&format=nameonly&persite=1&select='resptime>0\" -O ./planetnode.txt")

	print "I'm downloading the list of nodes and resolve IP addresses"

	x="./planetnode.txt"
	f=open(x,"r")
	allfile=f.readlines()
	f.seek(0,0)
	for linea in f.readlines():
		pathf="./hosts/"+linea[0:len(linea)-1];
		newf=open(pathf,"w")		
		xx="Address = "+socket.gethostbyname(linea[0:len(linea)-1])
		newf.write(xx);
		newf.close()

	f.close()

#MAIN

nodeonplanetlab()
os.popen("./start.sh")


