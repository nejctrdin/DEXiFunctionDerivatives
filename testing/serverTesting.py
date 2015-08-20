import urllib, urllib2
import threading
from time import time
from sys import argv

_REQ = "333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333001001111122222222122122222222233233223223233233333333000000011011222222112112222222222222222222222223333333\nv1,v2,v3,v4,v5,v6\n2,2,3,3,2,3"

URL = "http://localhost:5000/get_derivatives"

VALUES = {"function": _REQ}
DATA = urllib.urlencode(VALUES)

def worker():
    while True:
        t = time()
        req = urllib2.Request(URL, DATA)
        rsp = urllib2.urlopen(req)
        if rsp.getcode()!=200:
            print rsp.getcode()
        print time() - t


threads = []
for i in xrange(int(argv[1])):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
