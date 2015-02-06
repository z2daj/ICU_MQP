import sys
from socket import *
import threading
import time

print('Starting up GS module')

# Define the port that will be used by the GS for listing.
GSListenPort = 5005

udpListenSocket = socket(AF_INET, SOCK_DGRAM)
udpListenSocket.bind(('', GSListenPort)) #not sure what to do if the system says this is busy.

heardFromDrone = False
connectedDrones = []
threadList = []

def handleDroneConnection(address):
    try:
        tcpListenSocket = socket(AF_INET, SOCK_STREAM)
        tcpListenSocket.connect(address)
    except:
        connected = False
        print "invalid connection."
    else:
        connected = True
        print "connected to: " + str(tcpListenSocket.getpeername()[0])

    while connected:
        try:
            data = tcpListenSocket.recv(1024)
        except:
            connectedDrones.remove(address)
            connected = False
        else:
            print data + "recived data from drone:" + address[0]

        if len(data) == 0:
            connected = False
            print "connection to " + address[0] + " has been terminated on the drone side."

def udpListen():
    while True:
        data, addr = udpListenSocket.recvfrom(1024) # buffer size is 1024 bytes. Note that this is a blocking operation.
        
        #addr has the correct ip, but the wrong port so we use the port sent in the UDP message. 
        address = (addr[0], int(data))
    
        if address not in connectedDrones:
            heardFromDrone = True
            connectedDrones.append(address)
            print "message recived from a drone at address: " + address[0]
            t = threading.Thread(target=handleDroneConnection, name="drone:" + address[0], args=(address,))
            t.start()
            print "spawning new thread to handle drone data."
        print "udp loop."

udpThread = threading.Thread(target=udpListen, name="udpListener", args=())
print "starting the UDP listener."
udpThread.start()

while True:
    print "Drones connected = ", threading.active_count()-2
    time.sleep(1)

print "done"