import os
import sys
import socket
#this script make the host script for tincd

#MAIN#
lista=open("/fairvpn/hosts/nodes","r")
for linea in lista.readlines():
	try:
		ipaddress = linea.split()[0]
		hostname = linea.split()[1]
		if (".public" in hostname ):
			newhostname=hostname.split('.')[0]
			newfile = open("/fairvpn/hosts/"+newhostname,"w")
			output = "Address = "+ipaddress+"\n"
			newfile.write(output)
			newfile.close()
		else: 
			continue
	except:
		continue

lista.close()

		


