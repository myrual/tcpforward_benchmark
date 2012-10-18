#!/usr/bin/env python
# coding:utf-8

import sys
import os

import gevent
import gevent.monkey
import gevent.server
import gevent.queue

import re
import time
import collections

QUEUE_MAP = {}

def producer_handler(sock, address):
    myid = sock.recv(1024)
    while 1:
        data = sock.recv(8192)
        try:
            QUEUE_MAP[myid].put(data)
        except KeyError:
            pass

def consumer_handler(sock, address):
    myid = sock.recv(1024)
    QUEUE_MAP[myid] = queue = gevent.queue.Queue()
    while 1:
        data = queue.get()
        sock.send(data)

def main():
    producer_server = gevent.server.StreamServer(('', 44445), producer_handler)
    producer_server.start()
    consumer_server = gevent.server.StreamServer(('', 44444), consumer_handler)
    consumer_server.start()
    while True:
    	gevent.sleep(100)

if __name__ == '__main__':
    main()
