import DroneData
import droneNetClass
import io
import simpycam
import os

#note that unix uses this format instead: /img/test.jpg
filename = os.path.dirname(__file__) + '\\img\\test.jpg'
camera = simpycam.simpycam(filename)

image = camera.capture()
pose = (1, 2, 3, 4, 5, 6)
time = 5
sysTime = 6

data = DroneData.DroneData()
data.load(pose, time, sysTime, image)

data.gpsTime = 10

#stream = data.serialize()
stream = data.serialize()

#data2 = DroneData.DroneData()
data2 = DroneData.DroneData()
data2.deserialize(stream)

with io.open('data2img.jpg', 'wb') as file:
    file.write(data2.image)

