import sys, os, select, paramiko, socket

username =sys.argv[1]

privatekeyfile = os.path.expanduser('~/.ssh/planet-lab')
mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)

#read hosts from file

hosts = []
goodhosts=[]

hosts = [line.strip() for line in open("./nodes.txt")]

print hosts
print "start"
for host in hosts:
	print "connecting to %s" % host
	try:	
		s=socket.socket()
		s.settimeout(1)
		s.connect((host, 22))
		t = paramiko.Transport(s)
		t.connect(username=username,hostkey=None,password=None,pkey=mykey)
		print t.is_authenticated()
		if (t.is_authenticated()): 
			goodhosts.append(host)
		del t
	except Exception:
		print "Not Good"

print goodhosts

filegood = open("./good.txt","w")

for node in goodhosts:
	filegood.write(node+"\n")
filegood.close()



