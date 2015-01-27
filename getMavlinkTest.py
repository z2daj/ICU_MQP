#This script will serve as a test for receiving mavlink messages from the APM/PXHK, it's a POC

import sys
import os

# import the pymavlink library and set up for use on APM
d = os.getcwd()
d += '/mavlink/pymavlink'
sys.path.append(d)

import pymavlink

