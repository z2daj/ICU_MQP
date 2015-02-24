# Setup necessary imports for mavlink integration
import sys
import os
import socket
import time
import threading
from collections import deque

# import the pymavlink library and set up for use on APM/LLC
d = os.getcwd()
d += '/mavlink/pymavlink'
sys.path.append(d)

import mavlinkv10

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../'))


class dataCapture(object):
    '''This class captures pose data from MAVProxy and stores them in a buffer of samples
    '''

    # connect to mavproxy out-port for message access
    HOST = ''
    mavproxy_port = 14550
    address_of_mavproxy = (HOST, mavproxy_port)

    mavproxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mavproxy_sock.bind(address_of_mavproxy)

    # Create mavlink object and connect to socket
    mav = mavlinkv10.MAVLink(mavproxy_sock)

    sampleQ = deque(maxlen=15)  # store last 15 samples , if maxlen is exceeded, deque removes old samples from left

    def __init__(self):
        print 'Spawning Data Capture Thread'

        dataThread = threading.Thread(target=self.getData, name='dataCap', args=())
        dataThread.start()

    def getData(self):

        while True:

            att = True
            gps = True

            while att or gps:

                (data_from_mavproxy, address_of_mavproxy) = self.mavproxy_sock.recvfrom(1024)

                try:
                    decoded_message = self.mav.decode(data_from_mavproxy)
                except mavlinkv10.MAVError as e:
                    print 'Error: ', e

                if decoded_message:

                    if decoded_message.get_msgId() == mavlinkv10.MAVLINK_MSG_ID_GPS_RAW_INT and gps:
                        # print 'GPS Message Received'
                        gps_time = decoded_message.time_usec
                        lat = decoded_message.lat
                        lon = decoded_message.lon
                        alt = decoded_message.alt
                        gps = False

                    if decoded_message.get_msgId() == mavlinkv10.MAVLINK_MSG_ID_ATTITUDE and att:
                        # print 'Attitude Message Received'
                        pitch = decoded_message.pitch
                        roll = decoded_message.roll
                        yaw = decoded_message.yaw
                        att = False

            print 'Storing Pose...'
            sample = lat, lon, alt, pitch, roll, yaw, gps_time  # creates a pose sample and appends it to sample list

            self.sampleQ.append(sample)
            # print self.sampleQ.__len__()

            time.sleep(0.1)  # sleep for 100ms

    def getNextSample(self):
        return self.sampleQ.pop()  # return a sample

    def getClosestSample(self, time):
        sample = min(self.sampleQ, key=lambda x: abs(x[2] - time))  # this should eventually trim data
        self.sampleQ.remove(sample)
        return sample