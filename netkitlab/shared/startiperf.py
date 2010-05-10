import os
import sys
import socket
import random
import time
#generate random number
def generatenumber():
	return random.random()*5


	
def generatepareto():
	return random.paretovariate(1)


def generateseed():
	x=socket.gethostbyname(socket.gethostname())
	f=open("./iptmp.txt","w")
	f.write(x)
	f.close()
	cmd="md5deep iptmp.txt >> ./out.txt"
	os.system(cmd)	
	f=open("./out.txt","r")
	line=f.readline()
	line=line[0:4]
	seed=0
	for char in line:
		seed=seed+ord(char)
	return seed


def getnode():
	f=open("/etc/hosts","r")
	listsnode=f.readlines()
	x=listsnode[6:len(listsnode)-2]
	while(1):		
		indi=random.random()*len(x)
		indexofspace=x[int(indi)].index('#');
		l=x[int(indi)][:indexofspace]
		lind=l.index('\t');
		if( l[lind+1:len(l)-1] != "bootnode" and l[lind+1:len(l)-1]!= socket.gethostname() ):
			direct="./hosts/"+l[lind+1:len(l)-1]
			d=open(direct,"r")
			linea=d.readline()
			linea=linea[linea.index("=")+1:]
			print "Selezionato nodo ", l[lind+1:len(l)-1]
			d.close()
			f.close()
			return str(linea[0:len(linea)-1])


# MAIN #

random.seed(generateseed())

while(1):
	numK=int(generatepareto());
	nodo=getnode()
	cmd="iperf --num "+str(numK)+"M -y C  --client "+nodo+" >> reportiperf.txt"
	print "Invio ",str(numK),"Mbyte al nodo",nodo
	os.system(cmd)
	attesa=generatenumber()*60
	print "Tra ",str(int(attesa)),"secondi ripartiro"
	time.sleep(int(attesa))
