import sys
import time
from socket import *

class droneNetClass(object):
    """This class provides functions for interacting with the ICU network. 
    It should be run as it's own thread.
    
    At the moment this class should have threadding issues with the connection code
    where it will lock the parent thread as the connect loop will not return until a 
    connection is made. This is bad."""

    #Define the port that the ground station will be listening on.
    gsListenPort = 5005 
    gsConnected = False
    
    tcpServer = socket(AF_INET, SOCK_STREAM)
    sock = socket(AF_INET, SOCK_DGRAM) 

    #function that starts the network services and sets up the connection to the GS
    def __init__(self):
        #setup the TCP server
        self.tcpServer.bind(('', 0)) #allow the system to find the best network ip and socket
        self.tcpServer.listen(1)

        self.tcpIncomingSocket = self.tcpServer.getsockname()[1]

        #start the UDP broadcast
        self.sock.bind(('', 0))
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    
    #try to connect, return false if unable to do so. 
    def connect(self):
        self.sock.sendto(str(self.tcpIncomingSocket), ('<broadcast>', self.gsListenPort))
        try:
            conn, address = self.tcpServer.accept()
        except:
            print "no connection"
        else:
            self.gsConnected = True
            print "Connected to GS at:" + address[0]
            return conn

    #Given a connection, start sending data.
    """takes a connection and serial data to send.
    return an error if connection is not valid.
    return 1 if data sent."""
    def send(self, conn, data):
        try:
            conn.send(data)
        except:
            self.gsConnected = False
            return 0
        else:
            return 1
    
    def close(self, conn):
        try:
            conn.close()
        except:
            return 0
        else:
            return 1