#!/usr/bin/env python
# coding:utf-8

import sys
import os

import gevent
import gevent.server
import gevent.queue

CONNECTION_QUEUE = gevent.queue.Queue()
BUFFER_SIZE = 65536

def io_copy(source, dest):
    wfile = dest.makefile('wb', BUFFER_SIZE)
    while 1:
        wfile.write(source.recv(BUFFER_SIZE))

def forward():
    connection_map = {}
    while 1:
        myid, conn_type, conn = CONNECTION_QUEUE.get()
        if myid not in connection_map:
            connection_map[myid] = (conn_type, conn)
        else:
            _, conn_in_map = connection_map[myid]
            if conn_type:
                gevent.spawn(io_copy, conn, conn_in_map)
            else:
                gevent.spawn(io_copy, conn_in_map, conn)

def producer_handler(sock, address):
    myid = sock.recv(1024)
    CONNECTION_QUEUE.put((myid, 1, sock))

def consumer_handler(sock, address):
    myid = sock.recv(1024)
    CONNECTION_QUEUE.put((myid, 0, sock))

def main():
    producer_server = gevent.server.StreamServer(('', 44445), producer_handler)
    producer_server.start()
    consumer_server = gevent.server.StreamServer(('', 44444), consumer_handler)
    consumer_server.start()
    forward()

if __name__ == '__main__':
    main()

