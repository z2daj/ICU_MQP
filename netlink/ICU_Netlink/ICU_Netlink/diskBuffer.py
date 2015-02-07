import os
import io


class diskBuffer(object):
    """This class models an open queue using the hard disk.
    The data model for this class is to store an index of streams
    that are ready to be sent over the network. """

    startOfFileTag = "start_of_file"
    queueLength = 0

    dataRegistery = {} #dict of start location keyed on index position

    #make an init method that will create the folder/file at the given path
    def __init__(self, bufferFile):
        self.filename = bufferFile
        with io.open('self.filename', 'wb') as file:
            file.writelines(self.startOfFileTag)
            self.dataRegistery[0] = len(self.startOfFileTag)
            file.close()
        

    #create an add and a pop
    def enqueue(self, stream):




