#! /usr/bin/env python

tinc_cmd = "./tincd --config=./ --bypass-security "
myOverlayIP = "10.0.0.2"
#myOverlayIP = "10.%d.%d.%d" % (random.randint(1,254),random.randint(1,254),random.randint(1,254))
bootstrap = "160.80.0.254"
bootstrapName = "bootnode"
fanout = 2
