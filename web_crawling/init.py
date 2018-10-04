/usr/bin/pythonm

curl -s https://en.wikipedia.org/wiki/Main_Page| sed -n 's/.*href="\([^"]*\).*/\1/p'| grep ^http| sort -u
