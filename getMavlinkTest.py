#This script will serve as a test for receiving mavlink messages from the APM/PXHK, it's a POC


import sys
import os
import socket
import re
import select
import time

# import the pymavlink library and set up for use on APM
d = os.getcwd()
d += '/mavlink/pymavlink'
sys.path.append(d)

import mavlinkv10

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../'))

# prepare for UDP connections and such
HOST = ''
mavproxy_port = 12345

# now create the damn mavlink server
mavproxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mavproxy_sock.setblocking(0)
mavproxy_sock.bind((HOST, mavproxy_port))

mav_obj = mavlinkv10.MAVLink_message(mavproxy_sock)