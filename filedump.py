#This python script will check if the Pi is connected to a wireless network
#If it is, it will then initate a file transfer of all the files in
#the images output path, waiting for a confirmation before continuing to the
#next file
#WIP - writing structure for future functionality
#TODO - get rsync of files over when in range (how to test?)

import os
import time
import urllib2

cwd = os.getcwd()
imgDir = '/home/pi/Python/images'
groundStationIP = 'http://www.google.com/' #needs to be changed to actual GS ip
timeout = 2

def checkConnection(ip, tOut):
    print "Checking for wifi connection..."
    try:
        response = urllib2.urlopen(ip, timeout=tOut)
        print "We are connected!"
        #use info to do some commands to maintain connection, perhaps hover
        return True
    except urllib2.URLError as err: pass
    return False

if checkConnection(groundStationIP, timeout):
    os.chdir(imgDir)
    print "HERE"

    for file in os.listdir(imgDir):
        #this is where the rsync commands will be, once in a working test environment
        print file
