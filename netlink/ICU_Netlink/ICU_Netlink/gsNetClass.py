import sys
from socket import *
import threading
import time


from collections import deque

class gsNetClass(object):
    """this is a class that packages the functions of the netlink program."""
    # Define the port that will be used by the GS for listing.
    GSListenPort = 5005

    udpListenSocket = socket(AF_INET, SOCK_DGRAM)
    udpListenSocket.bind(('', GSListenPort)) #not sure what to do if the system says this is busy.

    connectedDrones = []

    #list of all the the drone that has been recived from ALL drones, but has not been processed yet.
    droneDataQueue = deque()

    def handleDroneConnection(self, address):
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
                #this should be a drone data object
                data = tcpListenSocket.recv(2048)
                print "recived data from drone:" + address[0]
                self.droneDataQueue.append((data, address[0]))
            except:
                print "connection lost"
                self.connectedDrones.remove(address)
                connected = False
            else:
                if len(data) == 0:
                    connected = False
                    print "connection to " + address[0] + " has been terminated on the drone side."

    def udpListen(self):
        while True:
            data, addr = self.udpListenSocket.recvfrom(1024) # buffer size is 1024 bytes. Note that this is a blocking operation.
        
            #addr has the correct ip, but the wrong port so we use the port sent in the UDP message. 
            address = (addr[0], int(data))
    
            if address not in self.connectedDrones:
                self.connectedDrones.append(address)
                print "message recived from a drone at address: " + address[0]
                t = threading.Thread(target=self.handleDroneConnection, name="drone:" + address[0], args=(address,))
                t.start()
                print "spawning new thread to handle drone data."
            time.sleep(0.1)

    def __init__(self):
        udpThread = threading.Thread(target=self.udpListen, name="udpListener", args=())
        print "starting the UDP listener."
        udpThread.start()
        print "UDP listener running"

    def getAllData(self):
        return self.droneDataQueue
    
    def getData(self):
        return self.droneDataQueue.popleft()

    def numData(self):
        return len(self.droneDataQueue)

    def getConnected(self):
        return self.connectedDrones