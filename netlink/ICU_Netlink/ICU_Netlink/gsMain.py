import gsNetClass
import io
import os
import threading
import time

saveFolder = os.path.dirname(os.path.realpath(__file__)) 
if os.name == 'nt':#use windows style
    saveFolder = saveFolder + '\\data\\'
else:#use unix style
    saveFolder = saveFolder + '/data/'

network = gsNetClass.gsNetClass()

maxbufsize = 0
while True:
    if network.numData() > 0:
        data = network.getData()
        print "data recived"