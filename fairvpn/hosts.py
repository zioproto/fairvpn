import os
import sys
import socket
#this script make the host script for tincd

#MAIN#
lista=open("/fairvpn/hosts/nodes","r")
for linea in lista.readlines():
	try:
		if (linea.split()[0][0] == 1)
			ipaddress = linea.split()[0]
			hostname = linea.split()[1]
		else 
			continue
		newfile = open("/fairvpn/hosts/"+hostname,"w")
		output = "Address = "+ipaddress
		newfile.write(output)
		newfile.close()
	except:
		continue

lista.close()

		


