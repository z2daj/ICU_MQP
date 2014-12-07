# this script will connect to an FTP server hosted by the Pi
# our transfer will simply connect to the FTP server and pull all the files
# currently present in the image capture directory and store them locally

import ftplib
import os
import sys

#create instance of FTP class
ftps = ftplib.FTP('1.4.19.175')

#connect to the host on port 22 for a secure connection
ftps.connect('1.4.19.175', 22)


#  need to make sure i can connect to the ftp server running on the pi using the above commands
#  and then get a list of files from images directory. afterwards, transfer the files to a local
#  directory and do some file housekeeping on the remote directory to make sure space is maintained
#  maybe do a detection of space available and limit the number of images taken at any given time
#  to that number, or just roll with it depending on how the surveying goes.
