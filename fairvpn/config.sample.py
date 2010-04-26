#! /usr/bin/env python

tinc_cmd = "./tincd --config=./ --bypass-security -d2 -D"
myOverlayIP = ""
#myOverlayIP = "10.%d.%d.%d" % (random.randint(1,254),random.randint(1,254),random.randint(1,254))
bootstrap = "160.80.81.106"
bootstrapName = "x10x0x30x1"
fanout = 2
