import os
import sys
import socket
if(len(sys.argv)<2):
	print "bad command: type %s <path file>" %sys.argv[0]
	sys.exit(1)	
else:
	measure=open(sys.argv[1],"r")
#	dictio = {}
	dicti=[]
	count=0
	f=open("./good-bw-nodes.txt","w")
	for line in measure.readlines():
		bit=line.split('\t')
		
		
		if(int(bit[1].strip())>=1000000):
			if(bit[0].split('-')[0] not in dicti):
				dicti.append(bit[0].split('-')[0])
				f.write(bit[0].split('-')[0]+"\n")
		if(bit[0].split('-')[1] not in dicti):
				dicti.append(bit[0].split('-')[1])
				f.write(bit[0].split('-')[1]+"\n")
				

	
	print dicti
	f.close()
	measure.close()
			
	
