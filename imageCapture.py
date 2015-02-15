import simpycam #replace this and all calls to it with picamera for testing on the pi.
import time
import threading
from collections import deque

class imageCapture(object):
    """this class spawns threads to handle the image capture from the picam.
    The overall flow of this program is to capture images and load them into a queue.
    The data from the queue can be retrived by the calling thread."""

    """encdodes data in the format of (time_as_float , image_as_ByteIO)"""
    imageq = deque(maxlen = 10) #about 25MB of ram used for this...

    """"this should be run in its own thread."""
    def captureToQ(self):
        print "started capture"
        camera = simpycam.simpycam(self.filename)
        buf = camera.capture()
        while True:#this module should run until shutdown by master.
            time.sleep(0.75) #sleep for 3/4 of a second to simulate the picam
            self.imageq.append((time.time(), buf))
            #print "image added to queue at position:" + str(len(self.imageq))

    def getImage(self):
        """returns a (time_as_float , image_as_ByteIO) tuple"""
        return self.imageq.popleft()
    
    def hasImage(self):
        return len(self.imageq) > 0

    def __init__(self, filename):
        self.filename = filename
        print "starting capture thread"
        captureThread = threading.Thread(target=self.captureToQ, name="imageCaptureThread", args=())
        captureThread.start()