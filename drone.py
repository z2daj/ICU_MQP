#this is a working test for creating the general "drone" class structure
#TODO: add more functions and implement them

import picamera
import os

class Drone:
    #will contain 'current' pose information and image capturing abilities
    def __init__(self):
        self.pose = 0 #current pose information (from LLC)
        self.mode = '' #current mode [loiter auto guided stablize] (from LLC)
        self.camera = picamera.PiCamera() #init camera
        self.type = '' #drone type [fixed multiRotor]
        self.ip = '' #ip for comms
        self.currWP = '' #current waypoint


    def updatePose(self):
        #connect to LLC and grab pose info


    def loadMission(self, mission):
        #load mission coordinates from file/from stream to LLC
        
    
