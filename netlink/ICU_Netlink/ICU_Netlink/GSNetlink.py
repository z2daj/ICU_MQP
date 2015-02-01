import sys
import time
from socket import *

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
    
    #addr has the correct ip, but the wrong port so we use the port sent in the UDP message. 
    address = (addr[0], int(data))
    
    if address not in connectedDrones:
        heardFromDrone = True
        connectedDrones.append(address)
        print "message recived from a drone at address: " + address[0]

#at this point we have heard from the drone and are ready to start a tcp link to the provided socket.
tcpListenSocket = socket(AF_INET, SOCK_STREAM)
tcpListenSocket.connect(address)

print "connected to: " + str(tcpListenSocket.getpeername()[1])
print "at address: " + str(tcpListenSocket.getsockname()[1])

while True:
    data = tcpListenSocket.recv(1024)
    print data