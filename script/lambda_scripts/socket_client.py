import getch
import socket               # Import socket module
import sys

##########################<NOT BEING USED>##############################
########################################################################
########################################################################
########################################################################


def main():
    #global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
    #host = socket.gethostname() # Get local machine name
    host = socket.gethostname()
    port =12000                # Reserve a port for your service.
    print 'hello'
    s.connect(('68.130.128.2', port))
    run = True
    while run:
        input_char = getch.getch()
