rsync --daemon 
tincd --bypass-security --config=. -K -d2 -D<<EOF


EOF
tincd --bypass-security --config=. -d2 -D
