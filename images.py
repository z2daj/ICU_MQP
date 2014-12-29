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
import sys

camera = picamera.PiCamera()
cwd = os.getcwd()
time = time.time()  # doesn't do anything, just to make things happy
imgDir = cwd + '/images'
imgPath = imgDir + '/'
runTime = 60  # arbitrary capture time, should capture images for a minute
sleepTime = 0.25  # sleep time for individual frame captures
sockBuff = 4096

sz = 0
size = 0

#set up server socket for connections
HOST = ''
PORT = 5007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)  # should only be one client at a time, but made 2 for debugging purposes
(conn, addr) = s.accept()
print 'Connected by: ', addr


def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1:.2f}% {2}".format("#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def countFiles(dir):
    return len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])


fileCount = countFiles(imgDir)

print fileCount

while True:

    req = conn.recv(sockBuff)

    if req == 'name':
        files = os.listdir(imgDir)

        name = files[0]
        print name

        conn.send(name)

    if req == 'size':
        with open(imgPath + name, 'r') as f:

            size = os.path.getsize(f.name)
            conn.send(str(size))
            print size

    if req == 'img':
        with open(imgPath + name, 'r') as f:
            for line in f:
                if not line:
                    break

                conn.send(line)

                sz += float(len(line))

                update_progress(sz/size)

        f.close()
        conn.send('done')

    if req == 'close':
        conn.send('closing')
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        break

s.shutdown(socket.SHUT_RDWR)
s.close()

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