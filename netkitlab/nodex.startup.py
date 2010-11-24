#! /usr/bin/env python
import string
import sys
import os

for n in range(21,51):
	string = """ip link set up dev eth0
ip a a 160.80.0.%.2d/24 dev eth0""" % (n)
	filename = "node%.2d.startup" % (n)
	
	dirname = "mkdir node%.2d" % (n)
	
	os.system(dirname)

	f = open(filename,"w")
	f.write(string)
	f.close()


