import time
import socket

fileptr = open('MillionWeblinks.txt', 'r')
lines = fileptr.readlines()
for l in lines:
    l = l.strip()
    try:
        hostname, aliaslist, ipaddrlist = socket.gethostbyname_ex(l)
    except Exception as e:
        #print l, e
        continue
    print l, len(aliaslist), ' '.join(aliaslist), len(ipaddrlist), ' '.join(ipaddrlist)
    time.sleep(2)
