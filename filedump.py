# this script connects to an open socket on the Pi and initiates image transfers
# TODO: create directory for transfer results
# TODO: create received files from filename and read in data to form complete image
# TODO: do some kind of constant pinging of the server for dropped connection correction

#TODO: write a general send request function, and perform necessary actions based on that return

import os
import socket
import subprocess
import re

#setup some variables
currDir = os.getcwd()
gsIP = '1.4.19.116'  # needs to be updated to actual GS IP, probably of the 192.168.1.x variety
droneIP = '1.4.19.175'  # needs to be updated to actual drone IP
regex = '([0-9./])'  # regular expression for parsing ping statistics from ping output
sockBuff = 4096

#set up client socket for remote connection
PORT = 5007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#method to request filename from server
def requestImageName(sock):

    sock.send('name')
    name = sock.recv(sockBuff)

    return name


def requestImage(sock, name):

    sock.send('img')

    img = sock.recv(sockBuff)

    while img:
        with open(name, 'wb') as f:
            print 'Data: ' + img
            f.write(img)
        img = sock.recv(sockBuff)

    print 'Received image: ' + name

    
def sendRequest(sock, req):
    sock.send(req)
    ret = sock.recv(sockBuff)

    return ret

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

        filename = requestImageName(s)

        print filename

        requestImage(s, filename)

        sendRequest(s, 'close')

        s.close()


elif rc == 2:
    print('Drone1 with IP: %s did not respond' % droneIP)

else:
    print('Drone1 with IP: %s returned an error' %droneIP)