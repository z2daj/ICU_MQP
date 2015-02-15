#note that this module will only run on the raspberry pi because of this import. 
#in the future this should be abstracted into a module that will use the picam if present, 
#or some other camera (or file) otherwise.
import picamera
import io
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
        print "started capture thread"
        camera = picamera.PiCamera()
        camera.resolution = camera.MAX_RESOLUTION
        buf = io.BytesIO()
        while True:#this module should run until shutdown by master.
            camera.capture(buf, format='jpeg')
            self.imageq.append((time.time(), buf))

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