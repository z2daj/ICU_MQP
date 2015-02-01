
import sys
import time
import DroneLinkDatagram
from socket import *
import cPickle as pickle
print('Starting up GS module')

# Define the port that will be used by the GS for listing.
GSListenPort = 5005


udpListenSocket = socket(AF_INET, SOCK_DGRAM)
udpListenSocket.bind(('', GSListenPort)) #not sure what to do if the system says this is busy.
heardFromDrone = False

connectedDrones = []

print "starting UDP listen"
while not heardFromDrone:
    data, addr = udpListenSocket.recvfrom(1024) # buffer size is 1024 bytes. Note that this is a blocking operation.

    #addr has the correct ip, but the wrong port.

    droneLink = pickle.loads(data)

    if type(droneLink) == DroneLinkDatagram.DroneLinkDatagram:
        print "droneLink data detected"
        if addr not in connectedDrones and droneLink.getMsg() == "connect":
            heardFromDrone = True
            connectedDrones.append(addr)
            print "message recived from a drone at address: " + addr[0]

#at this point we have heard from the drone and are ready to start a tcp link to the provided socket.
tcpListenSocket = socket(AF_INET, SOCK_STREAM)
tcpListenSocket.connect((addr[0], droneLink.getAddr()[1]))

print "connected to: " + str(tcpListenSocket.getpeername()[1])
print "at address: " + str(tcpListenSocket.getsockname()[1])

while True:
    data = tcpListenSocket.recv(1024)
    print data