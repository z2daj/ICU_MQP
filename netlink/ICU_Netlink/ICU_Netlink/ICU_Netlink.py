import DroneData
import droneNetClass
import simDataCapture
import io
import simpycam
import os
import pickle


#filename = os.path.dirname(__file__) 
#if os.name == 'nt':#use windows style
#    filename = filename + '\\img\\test.jpg'
#else:#use unix style
#    filename = filename + '/img/test.jpg'


#test file right and read.
data = ("some data", 12, 123121.23123)

with io.open("filename.txt", 'wb') as file:
    pickle.dump(data, file)
    file.close()

with io.open("filename.txt", 'rb') as file:
    newData = pickle.load(file)
    file.close()

print data == newData