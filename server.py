#! /user/bin/python

from OSC import OSCServer
import sys
from time import sleep

server = OSCServer( ("localhost", 7110) )
server.timeout = 0
run = True

def handle_timeout(self):
    self.timed_out = True

import types
server.handle_timeout = types.MethodType(handle_timeout, server)

def payload_callback(path, tags, args, source):
    idx = 0

    while idx < len(args):
        print "{ (" + str(args[idx]) + ", " + str(args[idx + 1]) + ") " + str(args[idx + 2]) + " " + str(args[idx + 3]) + " }"
        idx += 4

def config_callback(path, tags, args, source):
    print "Height: " + str(args[0]) + " Width: " + str(args[1])
    print "Span: " + str(args[2])
    print "MinThreshold: " + str(args[3]) + " MaxThreshold: " + str(args[4])

def quit_callback(path, tags, args, source):
    global run
    run = False

server.addMsgHandler( "/payload", payload_callback )
server.addMsgHandler( "/config", config_callback )
server.addMsgHandler( "/quit", quit_callback )

def each_frame():
    server.timed_out = False
    while not server.timed_out:
        server.handle_request()

while run:
    each_frame()

server.close()
