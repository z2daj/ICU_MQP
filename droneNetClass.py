import sys
import time
import struct
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
    udpSock = socket(AF_INET, SOCK_DGRAM)

    #function that starts the network services and sets up the connection to the GS
    def __init__(self):
        print 'Initializing network connection...'
        #setup the TCP server
        self.tcpServer.bind(('', 0)) #allow the system to find the best network ip and socket
        self.tcpServer.listen(1)

        self.tcpIncomingSocket = self.tcpServer.getsockname()[1]

        #start the UDP broadcast
        self.udpSock.bind(('', 0))
        self.udpSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    
    #try to connect, return false if unable to do so. 
    def connect(self):

        print 'inside droneNetClass.connect()'
        self.tcpServer.setblocking(0)
        self.udpSock.sendto(str(self.tcpIncomingSocket), ('<broadcast>', self.gsListenPort))
        try:
            conn, address = self.tcpServer.accept()
        except Exception as e:
            print e
            print "no connection"
        else:
            self.gsConnected = True
            print "Connected to GS at:" + address[0]
            self.connection = conn

    #Given a connection, start sending data.
    """takes serial data to send.
    return an error if connection is not valid.
    return 1 if data sent."""
    def send(self, data):
        msg = struct.pack('>I', len(data)) + data
        sent = 0

        print 'inside droneNetClass.send(), gsConnected = ', self.gsConnected

        if not self.gsConnected:
            self.connect()

        try:
            starttime = time.time()
            sent = self.connection.send(msg)
            print str(sent) + " bytes sent in " + str(time.time()-starttime) + " seconds."
            return 1
        except Exception as e:
            print e
            print "error sending, " + str(sent) + " bytes send out of " + str(len(data))
            self.gsConnected = False
            return 0

    def close(self):
        try:
            self.connection.close()
        except:
            print "something went wrong when closing the socket"