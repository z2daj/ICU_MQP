import droneNetClass
from simDataCapture import simDataCapture
import io
import os
import time
from collections import deque
import cPickle as pickle

dataq = deque() #dataStream
backlog = deque() #filename

#setup the groundstation connection
network = droneNetClass.droneNetClass()

dataCapture = simDataCapture()

#send the data if network connected, save to disk otherwise
def sendData(someData):
    if not network.send(data):
        #the send failed, save the data for later 
        filename = str(time.time()) + ".dronedata"
        with io.open(filename, 'wb') as file:
            pickle.dump(data, file)
        backlog.append(filename)

#now that we have that out of the way, we can start working
#on the main program loop.
lastOldTime = 0
while True:
    #add a new datapoint to the send queue
    if len(dataCapture.samples):
        dataPacket = str(dataCapture.getNextSample())
        dataq.append(dataPacket)
        print dataPacket
    
    #send that data over the network / save to disk if no connection
    if len(dataq):
        data = dataq.popleft()
        sendData(data)
    
    if len(backlog) and network.gsConnected and (time.time()-lastOldTime) > 0.1:
        lastOldTime = time.time()
        filename = backlog.popleft()
        #load the contents of the backlog into memory
        with io.open(filename, 'rb') as file:
            oldData = pickle.load(file)
        os.remove(filename)#delete the old file from disk
        dataq.append(oldData)