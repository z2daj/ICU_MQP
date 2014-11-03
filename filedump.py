#This python script will run on the GS (Ground-Station)
#it will check to see if it can see any drones with the designated IP via PING
#and if the PING latency is below 200ms (arbitrarily chosen, should test to determine appropriate threshold)
#it will then initiate an rsync transfer of pictures stored in ~/Python/images to the machine's desktop
#TODO - implement handshake between pi and GS to confirm transfer of files is complete
#TODO - perhaps do files one at a time instead of a massive dump, or create archives... need to test best method of delivery

import os
import subprocess
import re

#setup some variables
currDir = os.getcwd()
gsIP = '1.4.19.107' #needs to be updated to actual GS IP, probably of the 192.168.1.x variety
droneIP = 'www.google.com'#'1.4.19.115' #needs to be updated to actual drone IP, probably of the 192.168.1.x variety, and in a list of several drones
regex = '([0-9./])'

#ping the bastard and see if it's available
p = subprocess.Popen(['ping', '-c', '3', droneIP], stdout=subprocess.PIPE)
stdoutput,stderror = p.communicate()
#output = re.split('\n+', stdoutput)

rc = p.returncode

if rc == 0:
    print('%s active' % droneIP)

    #grab average ping - on the second to last line every time out of 9 line output (7)
    avgPingStr = stdoutput.splitlines()[7]

    #perform regex to capture min/avg/max/std-dev ping statistics
    reStr = re.findall(regex, avgPingStr)
    reStr = ''.join(reStr)

    #separate out each entry dilimited by '/' character
    reStr = reStr.split('/')

    #grab the average ping result in ms
    avgPingStr = reStr[4]
    avgPing = float(avgPingStr)

    if avgPing <= 250:
        #begin rsync here
        print avgPing


elif rc == 2:
    print('%s no response' % droneIP)

else:
    print('%s error' %droneIP)

