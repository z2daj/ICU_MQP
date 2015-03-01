import droneNetClass
from DroneData import DroneData
from imageCapture import imageCapture
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

#setup the image capture thread.
cameraPath = os.path.dirname(os.path.realpath(__file__)) 
if os.name == 'nt':#use windows style
    cameraPath = cameraPath + '\\img\\test.jpg'
else:#use unix style
    cameraPath = cameraPath + '/img/test.jpg'
capture = imageCapture(cameraPath)

#send the data if network connected, save to disk otherwise
def sendData(someData):
    if not network.send(someData):
        #the send failed, save the data for later 
        filename = str(time.time()) + ".dronedata"
        with io.open(filename, 'wb') as file:
            pickle.dump(someData, file)
        backlog.append(filename)

#now that we have that out of the way, we can start working
#on the main program loop.
lastOldTime = 0
while True:
    #add a new datapoint to the send queue
    if len(dataCapture.samples) and capture.hasImage():
        dd = DroneData()

        timeImg = capture.getImage()
        imuData = dataCapture.getClosestSample(timeImg[0])

        dd.image = timeImg[1]
        dd.pose = imuData[0]
        dd.gpsTime = imuData[1]
        dd.systemTime = imuData[2]

        dataq.append(dd.serialize())
        print "added packet at position:" + str(len(dataq)) + " at time:" + time.asctime()
    
    #send that data over the network / save to disk if no connection
    if len(dataq):
        data = dataq.popleft()
        sendData(data)
    
    #if there is stuff in the backlog and the network is now connected, start
    #adding the backlog data to the send queue. Not that this could overload the
    #queue if the backlog gets too long.
    if len(backlog) and network.gsConnected and (time.time()-lastOldTime) > 0.1 and len(dataq) < 5:
        lastOldTime = time.time()
        filename = backlog.popleft()
        #load the contents of the backlog into memory a 
        with io.open(filename, 'rb') as file:
            oldData = pickle.load(file)
        os.remove(filename)#delete the old file from disk
        dataq.append(oldData)