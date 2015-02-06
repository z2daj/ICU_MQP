import DroneData
import droneNetClass
import imageCapture
import simDataCapture
import io
import os

filename = os.path.dirname(__file__) + '\\img\\test.jpg'

#spawn the image collection thread(s)
capture = imageCapture.imageCapture()

#spawn the data collection thread(s)
mavData = simDataCapture.simDataCapture()

#setup the groundstation connection
network = droneNetClass.droneNetClass()

#now that we have that out of the way, we can start working
#on the main program loop. The logic goes 