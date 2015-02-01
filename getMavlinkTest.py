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

mav = mavlinkv10.MAVLink(mavproxy_sock)

# set the WP_RADIUS parameter on the MAV at the end of the link
mav.param_set_send(7, 1, "WP_RADIUS", 101)

# alternatively, produce a MAVLink_param_set object
# this can be sent via your own transport if you like
m = mav.param_set_encode(7, 1, "WP_RADIUS", 101)

# get the encoded message as a buffer
b = m.get_msgbuf()

# decode an incoming message
m2 = mav.decode(b)

# show what fields it has
print("Got a message with id %u and fields %s" % (m2.get_msgId(), m2.get_fieldnames()))

# print out the fields
print(m2)