#! /usr/bin/env python

tinc_cmd = "tincd --config=./ --bypass-security -d2 -D"
myOverlayIP = "10.0.0.8"
#myOverlayIP = "10.%d.%d.%d" % (random.randint(1,254),random.randint(1,254),random.randint(1,254))
bootstrap = "160.80.80.254"
bootstrapName = "x10x0x0x254"
fanout = 2
