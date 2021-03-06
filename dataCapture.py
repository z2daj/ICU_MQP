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

    sampleQ = deque(maxlen=100)  # store last 100 samples , if maxlen is exceeded, deque removes old samples from left

    debug = False  # allow for no APM connection over USB, fill pose information with default data

    def __init__(self, debug):

        self.debug = debug
        self.armed = self.isArmed()
        print 'Spawning Data Capture Thread'

        dataThread = threading.Thread(target=self.getData, name='dataCap', args=())
        dataThread.start()

    def getData(self):

        while self.armed:

            att = True
            gps = True

            while att or gps:

                if not self.debug:
                    (data_from_mavproxy, address_of_mavproxy) = self.mavproxy_sock.recvfrom(1024)

                    try:
                        decoded_message = self.mav.decode(data_from_mavproxy)
                    except mavlinkv10.MAVError as e:
                        # print 'Error: ', e
                        break

                    while att or gps:
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


                else:
                    if gps:
                        gps_time = 7
                        lat = 7
                        lon = 7
                        alt = 7
                        gps = False
                    if att:
                        pitch = 7
                        roll = 7
                        yaw = 7
                        att = False

            print 'Storing Pose...'
            pose = (lat, lon, alt, pitch, roll, yaw)
            sample =  (pose, gps_time, time.time()) # creates a pose sample and appends it to sample list

            self.sampleQ.append(sample)
            # print len(self.sampleQ)

            time.sleep(0.01)  # sleep for 10ms

    def isArmed(self):
        receivedArmed = False

        if not receivedArmed:
            (data_from_mavproxy, address_of_mavproxy) = self.mavproxy_sock.recvfrom(1024)

            try:
                decoded_message = self.mav.decode(data_from_mavproxy)
            except mavlinkv10.MAVError as e:
                # print 'Error: ', e
                break

            if decoded_message.get_msgId() == 128:  # 128 => MAV_MODE_FLAG_SAFETY_ARMED message ID
                receivedArmed = True

        return receivedArmed

    def getNextSample(self):
        return self.sampleQ.pop()  # return a sample

    def getClosestSample(self, time):
        sample = min(self.sampleQ, key=lambda x: abs(x[2] - time))
        trimData(sample)
        return sample

        #remove all of the data that came before the given sample.
    def trimData(self, sample):
        sampleTime = sample[2]
        for s in self.samples:
            if s[2] < sampleTime:
                self.samples.remove(s)