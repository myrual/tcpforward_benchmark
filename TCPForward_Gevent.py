#!/usr/bin/python

import gevent
from gevent import socket
from gevent.server import StreamServer
from gevent.queue import Queue

def InsertIDWithSocket(myid, mysocket, myglo_map):
	myglo_map[myid] = mysocket

glo_consumer_socket = {}
def producerForward(socket, address):
	fp = socket.makefile()
	destfp = ""
	myid = socket.recv(1024)
	gevent.sleep(0)
	while True:

		chunk = socket.recv(1024)
		if destfp == "":
			if myid in glo_consumer_socket:
				destfp = glo_consumer_socket[myid]
		else:
			destfp.send(chunk)
		gevent.sleep(0)

def consumerForward(socket, address):
	fp = socket.makefile()
	myid = socket.recv(1024)
	glo_consumer_socket[myid] = socket
	gevent.sleep(0)
	while True:
		gevent.sleep(100)
def startStreamServer(port, handle):
	ss = StreamServer(("", port), handle)
	ss.start()
	
serverProducer = StreamServer(("", 44445), producerForward)
serverProducer.start()
serverConsumer = StreamServer(("", 44444), consumerForward)
serverConsumer.start()
while True:
	gevent.sleep(100)
