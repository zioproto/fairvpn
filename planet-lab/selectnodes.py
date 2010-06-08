import os
import sys
import random
import socket
#MAIN#
if( len(sys.argv)<2):
	print "bad command: type python %s <number_of_nodes>" %sys.argv[0]
	sys.exit(1);
else:
	good=open("./goodnodes.txt","r")
	lista=good.readlines()
	try:
		usingnode=open("./usingnodes.txt","r+")	
		unode=usingnode.readlines()
		for i in range(int(sys.argv[1])):
			newnode=lista[random.randrange(0,len(lista)-1)]
			while  newnode in unode:
				newnode=lista[random.randrange(0,len(lista)-1)]
	
			usingnode.write(newnode)		
		usingnode.close()
		good.close()
	except IOError:
		usingnode=open("./usingnodes.txt","w")	
		usingnode.close()
		usingnode=open("./usingnodes.txt","r+")	
		unode=usingnode.readlines()
		for i in range(int(sys.argv[1])):
			newnode=lista[random.randrange(0,len(lista)-1)]
			while  newnode in unode:
				newnode=lista[random.randrange(0,len(lista)-1)]
	
			usingnode.write(newnode)		
			#print socket.gethostbyaddr(newnode[0:len(newnode)-1])[0]
		usingnode.close()
		good.close()
		
		
