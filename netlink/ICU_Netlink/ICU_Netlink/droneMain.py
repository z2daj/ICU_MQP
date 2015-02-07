import droneNetClass
import io
import os
import time
from collections import deque
import cPickle as pickle

dataq = deque() #dataStream
backlog = deque() #filename

#setup the groundstation connection
network = droneNetClass.droneNetClass()

#send the data if network connected, save to disk otherwise
def sendData(someData):
    if not network.send(data):
        #the send failed, save the data for later 
        filename = str(time.time()) + ".dronedata"
        with io.open(filename, 'wb') as file:
            pickle.dump(data, file)
        backlog.append(filename)
        print "sample added to backlog, length now:" + str(len(backlog))
    else:
        print "sample sent"

#now that we have that out of the way, we can start working
#on the main program loop.
lastTime = 0
lastOldTime = 0
while True:
    #add a new datapoint to the queue every second
    if time.time() - lastTime > 1:
        lastTime = time.time()
        dataq.append(time.asctime())
    
    #send that data over the network / save to disk if no connection
    if len(dataq):
        data = dataq.popleft()
        sendData(data)
    
    if len(backlog) and network.gsConnected and (time.time()-lastOldTime) > 0.5:
        lastOldTime = time.time()
        filename = backlog.popleft()
        #load the contents of the backlog into memory
        with io.open(filename, 'rb') as file:
            oldData = pickle.load(file)
        os.remove(filename)#delete the old file from disk
        #print "send old data:" + oldData
        #sendData(oldData)

        print "add old to queue:" + oldData 
        dataq.append(oldData)