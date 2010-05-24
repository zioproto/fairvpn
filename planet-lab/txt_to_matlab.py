import os
import sys

if(len(sys.argv)<2):
	print "bad command: type %s <file to modify>"% sys.argv[0]
	sys.exit(1)
else:
	errors=0
	done=0
	
	filetxt=open(sys.argv[1],"r")
	lines=filetxt.readlines();
	filetxt.close()
	
	alli=len(lines)

	filemat=open("./txtmatlab.txt","w")
	
	for linea in lines:
		linea=linea.split(',')
		if(linea[1] != "0.0.0.0" and linea[3]!="0.0.0.0"):
			filemat.write(linea[1]+"-"+linea[3]+"\t"+linea[8])
	
			done=done+1
		else:
			errors=errors+1

	filemat.close()
	
	print "Summary:"
	print "Write %d lines of %d" %(done, alli)
	print "%d lines are ignored" %errors
