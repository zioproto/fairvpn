rm -v ./bin/*
rm -v ./libs/*
cd olsrd/
tar -jxvf olsrd-0.6.0.tar.bz2
cd olsrd-0.6.0
make && make libs
cp olsrd ../../bin/
cp -v lib/*/olsrd_* ../../lib/
cd ../../
cd rsync/
tar -zxvf rsync-3.0.7.tar.gz
cd rsync-3.0.7
./configure LDFLAGS=-static && make
cp rsync ../../bin/
cd ../../
cd telnet
tar -jxvf telnet-bsd-1.2.tar.bz2
cd telnet-bsd-1.2
./configure LDFLAGS=-static && make
cp telnet/telnet ../../bin/
cd ../../
cd tinc
tar -zxvf tinc-1.0.13.tar.gz
cd tinc-1.0.13/src/
patch -p0 < ../../tinc-1.0.13-fairvpn.patch
cd ..
./configure LDFLAGS=-static && make
cp src/tincd ../../bin/

