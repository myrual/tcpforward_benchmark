#!/usr/bin/python
from twisted.internet import epollreactor
epollreactor.install()

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor


def InsertIDWithSocket(myid, mysocket, myglo_map):
	myglo_map[myid] = mysocket

glo_consumer_socket = {}
class producerForward(Protocol):

    def connectionMade(self):
	self.myid = ""

    def dataReceived(self, data):
	if self.myid == "":
		self.myid = data
	else:
		if self.myid in glo_consumer_socket:
			transport = glo_consumer_socket[self.myid]
			transport.write(data)

class consumerForward(Protocol):

    def connectionMade(self):
	self.myid = ""
    def connectionLost(self, reason):
	if self.myid <> "":
		del glo_consumer_socket[self.myid]

    def dataReceived(self, data):
	if self.myid == "":
		self.myid = data
		glo_consumer_socket[self.myid] = self.transport

class consumerFactory(Factory):
    def buildProtocol(self, addr):
        return consumerForward()

class producerFactory(Factory):
    def buildProtocol(self, addr):
        return producerForward()
reactor.listenTCP(44444, consumerFactory())
reactor.listenTCP(44445, producerFactory())

reactor.run()

