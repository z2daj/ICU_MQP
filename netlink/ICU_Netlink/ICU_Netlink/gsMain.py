import gsNetClass
import DroneData
import io
import os
import threading
import time
import xml.etree.cElementTree as ET

saveFolder = os.path.dirname(os.path.realpath(__file__)) 
if os.name == 'nt':#use windows style
    saveFolder = saveFolder + '\\data\\'
else:#use unix style
    saveFolder = saveFolder + '/data/'

network = gsNetClass.gsNetClass()

maxbufsize = 0
timeSinceLast = 0
while True:
    if network.numData() > 0:
        (data, ip) = network.getData()
        if data is not None:
            droneData = DroneData.DroneData()
            droneData.deserialize(data)

            print "data recived from drone: " + ip
            print "time since last rx: " + str(time.time() - timeSinceLast)
            timeSinceLast = time.time()

            if os.name == 'nt':
                dataFolder = saveFolder +  ip + '\\'
            else:
                dataFolder = saveFolder + ip + '/'

            if not os.path.exists(dataFolder):
                os.makedirs(dataFolder)

            saveFile = dataFolder + str(time.time())

            with io.open(saveFile + '.jpg', 'wb') as file:
                file.writelines(droneData.image)
             
            gpsTime = droneData.gpsTime
            sysTime = droneData.systemTime

            #now save the rest of the data as xml using the same name as the image.
            root = ET.Element("dronedata")
            pose = ET.SubElement(root, "pose")
            ET.SubElement(pose, "lat").text = str(droneData.pose[0])
            ET.SubElement(pose, "lon").text = str(droneData.pose[1])
            ET.SubElement(pose, "alt").text = str(droneData.pose[2])
            ET.SubElement(pose, "pitch").text = str(droneData.pose[3])
            ET.SubElement(pose, "roll").text = str(droneData.pose[4])
            ET.SubElement(pose, "yaw").text = str(droneData.pose[5])

            ET.SubElement(root, "gpsTime").text = str(droneData.gpsTime)
            ET.SubElement(root, "systemTime").text = str(droneData.systemTime)

            tree = ET.ElementTree(root)

            with io.open(saveFile + '.xml', 'wb') as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)

    time.sleep(0.1)