#This python script creates an images directory and will take pictures from
#the PiCamera every 10sec and store them with timestamps in the images
#directory

import os
import picamera
import time

camera = picamera.PiCamera()
cwd = os.getcwd()
imgDir = cwd + '/images'
runTime = (60)  # arbitrary capture time, should capture images for three minutes


FRAMES = 2500

camera.resolution = (2592, 1944)

#capture images to a specified output path with the timestamp as the filename
def captureImage(outputPath):
    if os.path.exists(outputPath):
        os.chdir(outputPath)
        timeStr = time.strftime("%Y%m%d-%H%M%S")
        camera.capture(timeStr + '.jpg')
        print "Image captured with filename: " + timeStr + ".jpg"

    else:
        print "Output path: " + outputPath + "doesn't exist."

#check to see if there is an existing output directory
print 'Checking if /images exists...'

if os.path.exists(imgDir):
    print "It exists!"

else:
    print "It doesn't exist, creating directory"

    os.makedirs(imgDir)
    
    print "Directory created."

# grab a start time
startTime = time.time()
currentTime = time.time()

# capture images for three minutes
while (currentTime - startTime) < runTime:

    print 'Time Difference: ' + (currentTime - startTime)
    print 'Run Time: ' + runTime

    #captures an image to imgDir
    for frame in range(FRAMES):
        captureImage(imgDir)
        time.sleep(0.25)

    currentTime = time.time()

print 'Done capturing images.'