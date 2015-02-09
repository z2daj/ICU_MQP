import gsNetClass
import DroneData
import io
import os
import threading
import time

saveFolder = os.path.dirname(os.path.realpath(__file__)) 
if os.name == 'nt':#use windows style
    saveFolder = saveFolder + '\\data\\'
else:#use unix style
    saveFolder = saveFolder + '/data/'

network = gsNetClass.gsNetClass()

maxbufsize = 0
while True:
    if network.numData() > 0:
        (data, ip) = network.getData()
        droneData = DroneData.DroneData()
        
        droneData.deserialize(data)
        print droneData.pose

        print "data recived from drone: " + ip
        
        if os.name == 'nt':
            dataFolder = saveFolder +  ip + '\\'
        else:
            dataFolder = saveFolder + ip + '/'

        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)

        saveFile = dataFolder + str(time.time()) + '.jpg'

        with io.open(saveFile, 'wb') as file:
            file.writelines(droneData.image)