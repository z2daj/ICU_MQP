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

# necessary variables for requesting data from APM, will be useful when we have more than one drone
# tgt_system = 0
# tgt_component = 0

# prepare for UDP connections and such
HOST = ''
mavproxy_port = 14550
address_of_mavproxy = (HOST, mavproxy_port)

# now create the damn mavlink server
mavproxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mavproxy_sock.bind(address_of_mavproxy)

# create a mavlink object which reads data from the mavproxy socket
mav = mavlinkv10.MAVLink(mavproxy_sock)

def getData():

    att = True
    gps = True
    data = []

    while att and gps:
        try:
            (data_from_mavproxy, address_of_mavproxy) = mavproxy_sock.recvfrom(1024)
            decoded_message = mav.decode(data_from_mavproxy)
        except Exception:
            pass

        if decoded_message.get_msgId() == mavlinkv10.MAVLINK_MSG_ID_GPS_RAW_INT and gps:
            gps_time = decoded_message.time_usec
            lat = decoded_message.lat
            lon = decoded_message.lon
            alt = decoded_message.alt
            gps = False

        if decoded_message.get_msgId() == mavlinkv10.MAVLINK_MSG_ID_ATTITUDE and att:
            time_since_boot = decoded_message.time_boot_ms
            pitch = decoded_message.pitch
            roll = decoded_message.roll
            yaw = decoded_message.yaw
            att = False

    pose = lat, lon, alt, pitch, roll, yaw
    time = gps_time, time_since_boot

    data.append(pose)
    data.append(time)

    return data

while True:

    pose = getData()[0]
    time = getData()[1]

    print 'Pose (lat, lon, alt, pitch, roll, yaw): ' % pose
    print 'Time (gps_usec, apm_boot_ms): ' % time



































# Useful shit if we need to request more data from APM
# print 'Received These Message IDs: '
# print gps
#
# gpsReq = True
# # create an encoded DATA_STREAM_ENCODE message with stream ID 6 (MAV_DATA_STREAM_POSITION)
# encoded_message = mav.request_data_stream_encode(1, 1, 6, 1, 1)
#
# print encoded_message
#
# mavproxy_sock.sendto(encoded_message.get_msgbuf(), address_of_mavproxy)
#
# tries = 0
# while gpsReq:
#
#     (data_from_mavproxy, address_of_mavproxy) = mavproxy_sock.recvfrom(1024)
#
#     try:
#         decoded_message = mav.decode(data_from_mavproxy)
#     except Exception as e:
#         pass
#
#     if decoded_message:
#         tries += 1
#         gps.append(decoded_message.get_msgId())
#
#     print 'Received Data Stream: '
#     print decoded_message
#
#     if tries == 50:
#         gpsReq = False
#
#
# print gps