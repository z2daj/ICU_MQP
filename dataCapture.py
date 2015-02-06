# Setup necessary imports for mavlink integration
import sys
import os
import socket

# import the pymavlink library and set up for use on APM
d = os.getcwd()
d += '/mavlink/pymavlink'
sys.path.append(d)

import mavlinkv10

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../'))

# all the socket stuff I'm leaving out here for the time being, presumably this will be taken care of elsewhere
HOST = ''
mavproxy_port = 14550
address_of_mavproxy = (HOST, mavproxy_port)

mavproxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mavproxy_sock.bind(address_of_mavproxy)


class dataCapture(object):
    '''This class captures pose data from MAVProxy and stores them in a buffer of samples
    '''

    samples = []

    # Create mavlink object
    mav = mavlinkv10.MAVLink(mavproxy_sock)

    def __init__(self):
        pose = self.getData()[0]
        time = self.getData()[1]

        sample = pose, time
        self.samples.append(sample)

        print pose
        print time

    def getData(self):

        att = True
        gps = True
        data = []

        while att or gps:

            (data_from_mavproxy, address_of_mavproxy) = mavproxy_sock.recvfrom(1024)

            try:
                decoded_message = self.mav.decode(data_from_mavproxy)
            except mavlinkv10.MAVError:
                pass

            if decoded_message:

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