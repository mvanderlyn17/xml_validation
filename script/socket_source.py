#!/usr/bin/env python

import sys
import os
import time
from socket import *

import code
import readline
import rlcompleter

sys.path.append('../src')

print 'Searching for devices'

serverPort = 12000
serverSocket = socket.socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('68.130.128.2',serverPort))
serverSocket.listen(1)
print "The server is ready to receive"
connectionSocket, addr = serverSocket.accept()
x=1
y=1
while 1:
   x=1
   if y==1:
       print "connected to ", addr
       y=0

   sentence = connectionSocket.recv(1024)
