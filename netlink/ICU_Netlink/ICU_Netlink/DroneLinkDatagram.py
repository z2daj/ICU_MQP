class DroneLinkDatagram(object):
    """this class packages the connection details for setting up the tcp link."""

    #create an init method to load data when the class is constructed. 
    def __init__(self, address, message):
        self.address = address
        self.message = message

    #override the equals and not equals functions
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.address == other.address
        else:
            return False

    def __ne__(self, other):
        return not self.address != other.address

    def getAddr(self):
        return (self.address)

    def getMsg(self):
        return self.message