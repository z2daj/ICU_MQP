from droneNetClass import droneNetClass
from DroneData import DroneData
from imageCapture import imageCapture
from simDataCapture import simDataCapture
#from dataCapture import dataCapture as dataCaptureClass
import io
import os
import time
from collections import deque
import cPickle as pickle

dataq = deque() #dataStreams
backlog = deque() #filenames

#setup the groundstation connection
network = droneNetClass()

#dataCapture = dataCaptureClass(True)
dataCapture = simDataCapture()

capture = imageCapture()

def saveToDisk(data):
    #the send failed, save the data for later
    startTime = time.time()
    filename = str(time.time()) + ".dronedata"
    with io.open(filename, 'wb') as file:
        pickle.dump(data, file)
        file.close()
    backlog.append(filename)
    print "added data to backlog at postion: " + str(len(backlog)) + " in " + str(time.time() - startTime)


#send the data if network connected, save to disk otherwise
def sendData(listOfData):
    startTime = time.time()
    length = len(listOfData)
    if not network.send(listOfData):
        for data in listOfData:
            saveToDisk(data)
    else:
        print "Sent " + str(length) + " elements in " + str(time.time() - startTime)


def main():
    lastOldTime = 0
    while True:
        #add a new datapoint to the send queue
        if len(dataCapture.samples) and capture.hasImage():
            dd = DroneData()

            timeImg = capture.getImage()
            imuData = dataCapture.getClosestSample(timeImg[0])

            print "image data time delta = " + str(timeImg[0] - imuData[2])

            dd.image = timeImg[1]
            dd.pose = imuData[0]
            dd.gpsTime = imuData[1]
            dd.systemTime = imuData[2]

            startTime = time.time()
            dataq.append(dd.serialize())
            print "added packet at position:" + str(len(dataq)) +" in "+ str(time.time() - startTime)
    
        #send that data over the network / save to disk if no connection
        if len(dataq) > 4:
            dataList = []
            length = len(dataq)
            for i in range(length):
                data = dataq.popleft()
                dataList.append(data)
            sendData(dataList)
    
        #if there is stuff in the backlog and the network is now connected,
        #start adding the backlog data to the send queue. 
        if len(backlog) and network.gsConnected and (time.time() - lastOldTime) > 0.1 and len(dataq) < 15:
            lastOldTime = time.time()
            filename = backlog.popleft()
            #load the contents of the backlog into memory a
            with io.open(filename, 'rb') as file:
                oldData = pickle.load(file)
                file.close()
            os.remove(filename)#delete the old file from disk
            dataq.append(oldData)
            print "added backlog item to dataq position: " + str(len(dataq)) + " in " + str(time.time() - lastOldTime)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
    