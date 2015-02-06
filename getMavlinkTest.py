#This script will serve as a test for receiving mavlink messages from the APM/PXHK, it's a POC


import sys
import os
import socket

# import the pymavlink library and set up for use on APM
d = os.getcwd()
d += '/mavlink/pymavlink'
sys.path.append(d)

import mavlinkv10

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../'))

# nececssary variables for requesting data from APM
tgt_system = 0
tgt_component = 0

# prepare for UDP connections and such
HOST = ''
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

# try:
decoded_message = mav.decode(data_from_mavproxy)
# except MAVError as e:
#     print e

# print('Got a message with id: %u, fields: %s, component: %d, System ID: %d' %(decoded_message.get_msgId(), decoded_message.get_fieldnames(), decoded_message.get_srcComponent(), decoded_message.get_srcSystem()))

tgt_system = decoded_message.get_srcSystem()
tgt_component = decoded_message.get_srcComponent()

print 'System ID: %d, Component: %d' % (tgt_system, tgt_component)

print 'Moving into test loop...'

IDs = []
loopStat = True
tries = 0

while loopStat:

    # try:
    decoded_message = mav.decode(data_from_mavproxy)
    # except MAVError as e:
    #     print e

    IDs[tries] = decoded_message.get_msgId()
    if decoded_message:
        tries += 1

    # some test code to see how to get GPS data from APM
    # see if it's broadcast and grab it if so
    # first gets the raw GPS data
    if decoded_message.get_msgId() == mavlinkv10.MAVLINK_MSG_ID_GPS_RAW_INT:
        print 'Received a GPS message'
        print('Got a message with id: %u, fields: %s, component: %d, System ID: %d' % (decoded_message.get_msgId(), decoded_message.get_fieldnames(), decoded_message.get_srcComponent(), decoded_message.get_srcSystem()))
        print 'Decoded Message: '
        print decoded_message
        loopStat = False

    # check for broadcast filtered GPS pose (fused GPS and accel), in GPS-frame format
    if decoded_message.get_msgId() == mavlinkv10.MAVLINK_MSG_ID_GLOBAL_POSITION_INT_COV:
        print 'Received GPS position'
        print('Got a message with id: %u, fields: %s, component: %d, System ID: %d' % (decoded_message.get_msgId(), decoded_message.get_fieldnames(), decoded_message.get_srcComponent(), decoded_message.get_srcSystem()))
        print 'Decoded Message: '
        print decoded_message
        loopStat = False

    if tries == 1000:
        loopStat = False

print 'Received These Message IDs: '
print IDs
gpsReq = True

while gpsReq:

    # create an encoded DATA_STREAM_ENCODE message with stream ID 6 (MAV_DATA_STREAM_POSITION)
    encoded_message = mav.request_data_stream_encode(1, 1, 6, 1, 1)
    mavproxy_sock.sendto(encoded_message, address_of_mavproxy)

    (data_from_mavproxy, address_of_mavproxy) = mavproxy_sock.recvfrom(1024)

    # try:
    decoded_message = mav.decode(data_from_mavproxy)
    # except MAVError as e:
    #     print e

    print 'Received Data Stream: '
    print decoded_message
    gpsReq = False
