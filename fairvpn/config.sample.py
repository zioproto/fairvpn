#! /usr/bin/env python

tinc_cmd = "/fairvpn/bin/tincd --config=./ --bypass-security -d2 -D"
myOverlayIP = ""
#myOverlayIP = "10.%d.%d.%d" % (random.randint(1,254),random.randint(1,254),random.randint(1,254))
bootstrap = "160.80.103.148"
bootstrapName = "bootnode"
fanout = 2
