import DroneData
import droneNetClass
import simDataCapture
import io
import simpycam
import os

#note that unix uses this format instead: /img/test.jpg
filename = os.path.dirname(__file__) + '\\img\\test.jpg'
camera = simpycam.simpycam(filename)

image = camera.capture()

mavData = simDataCapture.simDataCapture()

data = DroneData.DroneData()

data.gpsTime = 10

#stream = data.serialize()
stream = data.serialize()

#data2 = DroneData.DroneData()
data2 = DroneData.DroneData()
data2.deserialize(stream)

with io.open('data2img.jpg', 'wb') as file:
    file.write(data2.image)

#file io testing
a = "this is a test for write."
b = "cantalope"
with io.open('testfile.txt', 'wb') as file:
    file.writelines(a)
    file.close()

with io.open('testfile.txt', 'ab') as file:
    file.writelines(b)
    file.close()
    
