import DroneData
import gsNetClass
import io
import simpycam
import os

#list of connected drone ip's used for tracking incoming data.
drones = []

#check to make sure that the data from old runs is cleaned, 
#do this by checking for the existance of a file, and then complaining if it is there.
#once done, create a file for the new data.
path = os.path.dirname(__file__) + "\\data"
print path
if os.path.exists(path):
    raise Exception("please remove data from last run in location:" + path)
else:
    os.makedirs(path)

#then start up the network management class
network = gsNetClass.gsNetClass()

while True:
    if network.numData() > 0:
        data = network.getData()
        pickledData = data[0] #this should be a pickled DroneData object

        folderpath = os.path.join(path, data[1])

        if data[1] not in drones:
            drones.append(data[1])
            os.makedirs(folderpath)

        filepath = os.path.join(folderpath, time.time())

        #save the whole pickle to a file, image and all
        with io.open(filepath + '.pickledDroneData', 'wb') as file:
            file.write(pickledData)

        #now depickle the file, print some data, and save the image.
        droneData = DroneData.DroneData()
        droneData.deserialize(pickledData)

        print droneData.systemTime()
        with io.open(filepath + '.jpg', 'wb')as file:
            file.write(droneData.image)