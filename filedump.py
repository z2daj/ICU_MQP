# this script connects to an open socket on the Pi and initiates image transfers
# TODO: do some kind of constant pinging of the server for dropped connection correction
# TODO: make this easier to adapt for an object-oriented approach
# TODO: write a general send request function, and perform necessary actions based on that return

import os
import sys
import socket
import subprocess
import re

# setup some variables
currDir = os.getcwd()
resultsDir = currDir + '/resultImgs'
resultsPath = resultsDir + '/'
gsIP = '1.4.19.116'  # needs to be updated to actual GS IP, probably of the 192.168.1.x variety
droneIP = '1.4.19.175'  # needs to be updated to actual drone IP
regex = '([0-9./])'  # regular expression for parsing ping statistics from ping output
sockBuff = 4096

size = 2100000
global sz
files = []

# set up client socket for remote connection
PORT = 5007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# this function takes in a directory and checks if it exists
# and creates it if it doesn't
def check_directory(dir):
    if os.path.exists(dir):
        print 'Result Directory exists at: ' + dir
    else:
        os.mkdir(dir)


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


#method to request filename from server
def requestImageName(sock):

    sock.send('name')
    name = sock.recv(sockBuff)

    return name


# this function takes in a socket and name argument, and requests the server for file of 'name' and stores it locally
def requestImages(sock, name):

    sz = 0
    sock.send('img')

    res = sendRequest(sock, name)
    size = int(s.recv(sockBuff))
    print size

    if res == 'yes':
        # store in root for now to make debugging easier
        f = open(resultsPath + name, 'w')
        # f = open(name, 'w')

        img = sock.recv(sockBuff)

        while img != 'done':

            f.write(img)

            sz += float(len(img))

            update_progress(sz/size)

            img = sock.recv(sockBuff)

        sz = 0
        sys.stdout.flush()
        print 'Received image: ' + name
        f.close()

    else:
        print 'No file with name, ' + name + ', exists on drone.'


def requestImageList(sock):

    sock.send('list')
    name = sock.recv(sockBuff)

    while name != 'done':
        files.append(name)
        name = sock.recv(sockBuff)

    print 'Received file list.'

    
def sendRequest(sock, req):
    sock.send(req)
    ret = sock.recv(sockBuff)

    return ret


#check if results directory exists
check_directory(resultsDir)

#ping the bastard to see if it's available, and grab the command output
print 'Pinging Drone1...'
p = subprocess.Popen(['ping', '-c', '3', droneIP], stdout=subprocess.PIPE)
stdOutput, stdError = p.communicate()
rc = p.returncode

if rc == 0:
    print('Drone1 with IP: %s is active' % droneIP)

    #grab average ping - on the second to last line every time out of 9 line output (7)
    avgPingStr = stdOutput.splitlines()[7]

    #perform regex to capture min/avg/max/std-dev ping statistics
    reStr = re.findall(regex, avgPingStr)
    reStr = ''.join(reStr)

    #separate out each entry delimited by '/' character
    reStr = reStr.split('/')

    #grab the average ping result in ms
    avgPingStr = reStr[4]
    avgPing = float(avgPingStr)

    if avgPing <= 250:
        print 'The average ping to Drone1 is ' + avgPingStr + 'ms'

        print 'Connecting to Drone Server...'

        s.connect((droneIP, PORT))

        requestImageList(s)

        # filename = files[0]
        # requestImages(s, filename)

        while files.__len__():
            for filename in files:
                print filename
                requestImages(s, filename)
                files.remove(filename)

        print 'Received all files.'

        print files

        re = sendRequest(s, 'close')

        print re

        if re == 'closing':
            s.shutdown(socket.SHUT_RDWR)
            s.close()


elif rc == 2:
    print('Drone1 with IP: %s did not respond' % droneIP)

else:
    print('Drone1 with IP: %s returned an error' %droneIP)