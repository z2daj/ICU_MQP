# this script will connect to an FTP server hosted by the Pi
# our transfer will simply connect to the FTP server and pull all the files
# currently present in the image capture directory and store them locally

import ftplib
import os
import sys

