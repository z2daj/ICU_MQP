
import threading
import time
import random as r

class simDataCapture(object):
    """this class is a simulation for Zach J's MAV interface.
    It will spawn a thread that will wait a random amount of time, and 
    then fill the fields of a mav-data struct which will be later paired with
    images. This data will be loaded into a hashtable keyed on time."""

    samples = []

    def getData(self):
        while True:
            pose = (r.randint(), r.randint(), r.randint(), r.randint(), r.randint(), r.randint())
            gpsTime = time.time()
            systime = time.time()
            sample = (pose, gpstime, systime)
            self.samples.append(sample)
            time.sleep(r.random())

    def getNextSample(self):
        return self.samples[0] #return the oldest sample

    def getClosestSample(self, time):#this should eventually trim the data.
        return min(self.samples, key=lambda x:abs(x[2] - time))

    def __init__(self):
        dataThread = threading.Thread(target=self.getData, name="dataGen", args=(self))
        print "spawning data thread"
        dataThread.start()
        print "data thread started"