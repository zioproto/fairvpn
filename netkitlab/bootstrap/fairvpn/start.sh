rm /fairvpn/hosts/nodes
touch /fairvpn/hosts/nodes
/fairvpn/bin/rsync --daemon --config=/fairvpn/rsyncd.conf
/fairvpn/bin/olsrd -f /fairvpn/olsrd.conf
/fairvpn/bin/tincd --bypass-security --config=. -K -d2 -D<<EOF


EOF
/fairvpn/bin/tincd --bypass-security --config=. -d2 -D

