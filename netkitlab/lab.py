#! /usr/bin/env python
import string

for n in range(21,51):
	string = """node%.2d[0]="underlay"
node%.2d[mem]=32
""" % (n,n)
	print string


