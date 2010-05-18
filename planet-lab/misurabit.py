
#MAIN#
counter=0
totalbitrate=0
error=0
listanodi=open("./codeploy/nodes.txt","r")
for nodo in listanodi.readlines():
	path="./codeploy/newdir/"+nodo[0:len(nodo)-1]
	try:
		#print "esploro :"+path
		f=open(path,"r")
		
		for x in f.readlines():
			bit=x.split(',')
			#print "["+str(counter)+"] "+bit[8]
			totalbitrate=totalbitrate+int(bit[8])
			counter=counter+1
		f.close()			
			

	except IOError:
		error=1
		
listanodi.close()
if(counter!=0):
	bit_average=totalbitrate/counter

bit_avg_mb=bit_average/1000000
print "Esaminati "+str(counter)+" campioni\nThe avg Bit rate is: "+str(bit_avg_mb)+" Mbits/s      ||       "+ str(bit_average)+" bit/s"
