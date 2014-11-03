#This python script creates an images directory and will take pictures from
#the PiCamera every 10sec and store them with timestamps in the images
#directory

import os
import picamera
import time

camera = picamera.PiCamera()
imgDir = '/home/pi/Python/images'
cwd = os.getcwd()


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

#captures an image to imgDir
captureImage(imgDir)
