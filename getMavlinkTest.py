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
HOST = '127.0.0.1'
mavproxy_port = 14550
address_of_mavproxy = (HOST, mavproxy_port)

# now create the damn mavlink server
mavproxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavproxy_sock.setblocking(0)
mavproxy_sock.bind(('', 14550))

# create a mavlink object which reads data from the mavproxy socket
mav = mavlinkv10.MAVLink(mavproxy_sock)

# Call to receive data over UDP socket, 1024 is the buffer size
(data_from_mavproxy, address_of_mavproxy) = mavproxy_sock.recvfrom(1024)

try:
    decoded_message = mav.decode(data_from_mavproxy)
except MAVError as e:
    print e

print('Got a message with id: %u, fields: %s, component: %d, System ID: %d' %(decoded_message.get_msgId(), decoded_message.get_fieldnames(), decoded_message.get_srcComponent(), decoded_message.get_srcSystem()))

# Prints the entire decode message
print 'Decoded Message: '
print decoded_message