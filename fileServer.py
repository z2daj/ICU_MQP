# This python script will take a number of images based on desired time
# and then store them in an 'images' directory
# finally, for testing purposes, it will create a socket-ed connection through which these images will be transferred
# to the ground-station
# TODO: test logic for transferring files line by line.
# TODO: store lists of files transferred to separate file so same files aren't transferred in case of server crash

import os
import time
import socket
import sys


cwd = os.getcwd()
imgDir = cwd + '/images'
imgPath = imgDir + '/'

sockBuff = 4096

global sz
size = 0

# set up server socket for connections
HOST = ''
PORT = 5007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)  # should only be one client at a time, but made 2 for debugging purposes
(conn, addr) = s.accept()
print 'Connected by: ', addr


def update_progress(progress):
    barLength = 10  # Modify this to change the length of the progress bar
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

    print req

    if req == 'list\0':
        files = os.listdir(imgDir)

        for name in files:
            name += '\0'
            conn.send(name)
            print name
            # time.sleep(0.05)  # wait for buffer to be received before sending next name

        conn.send('done\0')

    if req == 'size\0':
        with open(imgPath + name, 'r') as f:

            size = os.path.getsize(f.name)
            conn.send(str(size))
            print size

    if req == 'img\0':

        sz = 0
        name = conn.recv(sockBuff)
        size = os.path.getsize(imgPath+name)

        print size

        if files.__contains__(name):
            conn.send('yes\0')
            print 'yes'

            while req != 'size?\0':
                req = conn.recv(sockBuff)

            conn.send(str(size)+'\0')
            print 'size'

            # time.sleep(0.01)

            while req != 'img?\0':
                req = conn.recv(sockBuff)

            with open(imgPath + name, 'r') as f:
                for line in f:
                    if not line:
                        break

                    conn.send(line)

                    sz += float(len(line))
                    update_progress(sz/size)

                sz = 0
                sys.stdout.flush()
                print 'File, ' + name + ', sent.'
                files.remove(name)
                fileCount -= 1
                f.close()
                # time.sleep(0.01)

                conn.send('done\0')
                print 'done'

        else:
            conn.send('no\0')
            print 'no'

    if req == 'close\0':
        conn.send('closing\0')
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        break

s.shutdown(socket.SHUT_RDWR)
s.close()