import sys, os, select, paramiko, socket

if(len(sys.argv)<2):
	print "bad command \ntype :python CheckSsh.py <username>"
	sys.exit(1)
else:

	username =sys.argv[1]

	privatekeyfile = os.path.expanduser('~/.ssh/planet-lab')
	mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)

	#read hosts from file

	hosts = []
	goodhosts=[]
	noauth = 0
	timeouts = 0
	
	hosts = [line.strip() for line in open("./nodes.txt")]

	print hosts
	print "start"
	for host in hosts:
		#print "connecting to %s" % host
		try:	
			s=socket.socket()
			s.settimeout(3)
			s.connect((host, 22))
			t = paramiko.Transport(s)
			t.connect(username=username,hostkey=None,password=None,pkey=mykey)
			#print t.is_authenticated()
			if (t.is_authenticated()): 
				goodhosts.append(host)
			del t
		except paramiko.AuthenticationException:
			noauth = noauth + 1
			print "connecting to %s" % host
			print "Authentication Exception %d" % noauth

		except socket.timeout:
			timeouts = timeouts + 1
			print "connecting to %s" % host
			print "Timeouts! %d" % timeouts

	print goodhosts
	
	print "\nAuthentication errors: %d\n" % noauth
	print "\nTimeout errors %d\n" % timeouts

filegood = open("./good.txt","w")

for node in goodhosts:
	filegood.write(node+"\n")
filegood.close()



