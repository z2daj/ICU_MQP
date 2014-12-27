# This python script will take a number of images based on desired time
# and then store them in an 'images' directory
# finally, for testing purposes, it will create a socketed connection through which these images will be transfered
# to the groundstation
# TODO: test logic for transferring files line by line.
#

import os
import picamera
import time
import socket

camera = picamera.PiCamera()
cwd = os.getcwd()
time = time.time()  # doesn't do anything, just to make things happy
imgDir = cwd + '/images'
imgPath = imgDir +'/'
runTime = 60  # arbitrary capture time, should capture images for a minute
sleepTime = 0.25  # sleep time for individual frame captures
sockBuff = 4096

#set up server socket for connections
HOST = ''
PORT = 5007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)  # should only be one client at a time, but made 2 for debugging purposes
(conn, addr) = s.accept()
print 'Connected by: ', addr

# while True:
req = s.recv(4096)

print req

if req.equals('name'):
    files = os.listdir(imgDir)

    name = files[0]
    print name

    s.send(name)




#prepare send every single picture line by line as a string (seems archaic, but hey, we'll see how it works)
for filename in os.listdir(imgDir):

    print(filename)
    # data = conn.recv(4096)
    conn.send(filename)

    # with open((imgPath+filename), 'rb') as f:
    #     for line in f:
    #         if not line:
    #             break
    #
    #         conn.send(line)
    #         print(line)

conn.close()

# while 1:
#     data = conn.recv(4096)  # buffer size of 4096 bytes
#     if not data:
#         break
#
#     conn.send(data)
#
# conn.close()


#
# #calculate number of frames needed to fill allotted time and round to nearest integer
# FRAMES = int(runTime * sleepTime)
#
# camera.resolution = (2592, 1944)
#
# #capture images to a specified output path with the timestamp as the filename
# def captureImage(outputPath):
#     if os.path.exists(outputPath):
#         os.chdir(outputPath)
#         timeStr = time.strftime("%Y%m%d-%H%M%S")
#         camera.capture(timeStr + '.jpg')
#         print "Image captured with filename: " + timeStr + ".jpg"
#
#     else:
#         print "Output path: " + outputPath + "doesn't exist."
#
# #check to see if there is an existing output directory
# print 'Checking if /images exists...'
#
# if os.path.exists(imgDir):
#     print "It exists!"
#
# else:
#     print "It doesn't exist, creating directory"
#
#     os.makedirs(imgDir)
#
#     print "Directory created."
#
#
# #captures images to imgDir
# for frame in range(FRAMES):
#     captureImage(imgDir)
#     time.sleep(sleepTime)
#
# print 'Done capturing images.'