import io
import cPickle as pickle

"""This class packages the IMU and image data for 
sending from the drone to the ground station."""
class DroneData(object):

    def __init__(self):
        self.pose = ()
        self.gpsTime = 0
        self.systemTime = 0
        self.image = None

    def load(self, pose, gpsTime, sysTime, image_buffer):
        self.pose = pose
        self.gpsTime = gpsTime
        self.systemTime = sysTime
        self.image = image_buffer
        print "loaded data into dd object."

    def serialize(self):
        #print "returning serial stream from dronedata"
        return pickle.dumps(self)

    """Sets all of the fields of the class equal to the """
    def deserialize(self, stream):
        input = pickle.loads(stream)
        self.pose = input.pose
        self.gpsTime = input.gpsTime
        self.systemTime = input.systemTime
        self.image = input.image