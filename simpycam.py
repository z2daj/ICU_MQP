import os
import io

class simpycam(object):
    """this class simulates the picamera class for the raspberry pi."""

    """init the class with the path to folder containing jpg image files."""
    def __init__(self, path):
        self.buffer = io.BytesIO()
        try:
            with io.open(path, 'rb') as file:
                self.buffer = file.read()
        except:
            print "path: %s does not esist." % path


    """Capture returns a ByteIO object containing the contents"""
    def capture(self):
        return self.buffer