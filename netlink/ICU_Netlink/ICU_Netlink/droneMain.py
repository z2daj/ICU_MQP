import DroneData
import droneNetClass
import imageCapture
import simDataCapture
import io
import os
from collections import deque

dataQueue = deque() #if this gets too long we need to start buffering to disk.

filename = os.path.dirname(__file__) 
if os.name == 'nt':
    filename = filename + '\\img\\test.jpg'
else:
    filename = filename + '/img/test.jpg'

#setup the groundstation connection
print "setting up network"
network = droneNetClass.droneNetClass()
while not network.gsConnected:
    connection = network.connect()
print "network connected to:"

#spawn the image collection thread(s)
print "starting image capture"
capture = imageCapture.imageCapture(filename)

#spawn the data collection thread(s)
print "starting data capture"
mavData = simDataCapture.simDataCapture()

#now that we have that out of the way, we can start working
#on the main program loop.
while True:
    if capture.hasImage():
        print "getting image"
        image = capture.getImage() #image is (time_as_float , image_as_ByteIO) tuple
        
        print "geting data"
        data = mavData.getClosestSample(image[0])

        print "packaging"
        droneDataPacket = DroneData.DroneData()
        droneDataPacket.load(data[0], data[1], data[2], image[1])

        print "serializing"
        dataStream = droneDataPacket.serialize()

        #save the data to the disk in case connection is lost.
        dataName = str(time.time()) + ".datapacket"
        with io.open(dataName, 'wb') as file:
            file.write(dataStream)
            file.close()

    #send that data over the network / save to disk if no connection
    if network.gsConnected:
        network.send(connection, dataStream)
    else:
        while not network.gsConnected:
            connection = network.connect()
