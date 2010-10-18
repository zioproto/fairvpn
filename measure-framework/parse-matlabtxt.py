import os
import sys
import socket
import random
import threading
from threading import Thread
import time
import math as math

def jain_index(x):

	# x is dict.values()        
        k=len(x)
        sum1=0
        sum2=0
        i=0 
        #sum1=math.fsum(x)
        for i in range(k):
                sum1=sum1+x[i]
                sum2=sum2+math.pow(x[i],2)
        sum1=math.pow(sum1,2)
        sum2=k*sum2
        ji = float(sum1/sum2)
        return ji

def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)

connections = {}

lista=open("./txtmatlab.txt","r")
for linea in lista.readlines():
	connection = linea.split('\t')[0]
	bw = float(linea.split('\t')[1].strip('\n'))
	try:
		connections[connection].append(bw)
	except:
		connections[connection]=[bw]

lista.close()

print len(connections)

avdict = connections.copy()

for k,v in connections.iteritems():
	#print v
	theaverage = average(v)
	avdict[k] = theaverage
	print "%s\t%s" % (k, theaverage)

print jain_index(avdict.values())	





