import sys
from gevent import monkey; monkey.patch_socket()
import threading
import time
import urllib
import urllib2
import json
import unittest

import gevent
from gevent import socket
from gevent import Greenlet
from gevent.pool import Group
from gevent import monkey; monkey.patch_socket()

targetServer = "targetServer.com"

class TCPConsumerForward(Greenlet):
    def __init__(self):
	Greenlet.__init__(self)
    def insert(self, myid, Mark, myevent):
	self.ConsumerID = myid
	self.mark = Mark
	self.myevent = myevent
    def _run(self):
        curTime = time.gmtime()
	thisID = self.ConsumerID
	pp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pp.connect((targetServer, 44444))
	pp.send(thisID)
	gevent.sleep(1)

	while True:
	    pp.recv(19000)

class TCPProduction(Greenlet):
    def __init__(self):
	Greenlet.__init__(self)
    def insertID(self, myid, myevent):
	self.producerID = str(myid)
	self.myevent = myevent

    def _run(self):
	curTime =  time.gmtime()
	thisID = str(curTime.tm_min) + str(curTime.tm_sec) + self.producerID


	pp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pp.connect((targetServer, 44445))
	pp.send(thisID)
	gevent.sleep(1)

	aa = TCPConsumerForward()
	aa.insert(thisID, "first", self.myevent)
	aa.start()

	while True:
	    pp.send("V" * 6000)
	    gevent.sleep(delay)


if __name__ == "__main__":
	argvv = sys.argv[1:]
	threadpool = Group()

	delay = 0.1
	if argvv == []:
		count = 130
	else:
		if len(argvv) >= 1:
			count = int(argvv[0])
		if len(argvv) >= 2:
			delay = int(argvv[1])
	for i in xrange(count):
		print "Current Process " + str(i)
		webserverWorkingEvent = gevent.event.Event()
		j = TCPProduction()
		j.insertID(i, webserverWorkingEvent)
		threadpool.add(j)
		threadpool.start(j)
	threadpool.join()
