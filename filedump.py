#This python script will run on the GS (Ground-Station)
#it will check to see if it can see any drones with the designated IP via PING
#and if the PING latency is below 200ms (arbitrarily chosen, should test to determine appropriate threshold)
#it will then initiate an rsync transfer of pictures stored in ~/Python/images to the machine's desktop
#TODO - implement handshake between pi and GS to confirm transfer of files is complete
#TODO - perhaps do files one at a time instead of a massive dump, need to test best method of delivery

import os
import subprocess
import re

#setup some variables
currDir = os.getcwd()
gsIP = '1.4.19.107'  # needs to be updated to actual GS IP, probably of the 192.168.1.x variety
droneIP = '1.4.19.115'  # needs to be updated to actual drone IP
regex = '([0-9./])'  # regular expression for parsing ping statistics from ping output

#ping the bastard to see if it's available, and grab the command output
print 'Pinging Drone1...'
p = subprocess.Popen(['ping', '-c', '3', droneIP], stdout=subprocess.PIPE)
stdOutput, stdError = p.communicate()
rc = p.returncode

if rc == 0:
    print('Drone1 with IP: %s is active' % droneIP)

    #grab average ping - on the second to last line every time out of 9 line output (7)
    avgPingStr = stdOutput.splitlines()[7]

    #perform regex to capture min/avg/max/std-dev ping statistics
    reStr = re.findall(regex, avgPingStr)
    reStr = ''.join(reStr)

    #separate out each entry delimited by '/' character
    reStr = reStr.split('/')

    #grab the average ping result in ms
    avgPingStr = reStr[4]
    avgPing = float(avgPingStr)

    if avgPing <= 250:
        print 'The average ping to Drone1 is ' + avgPingStr + 'ms'
        print 'Starting rsync transfer...'

        print os.getcwd()
        subprocess.call(['./rsync.sh', droneIP])

elif rc == 2:
    print('Drone1 with IP: %s did not respond' % droneIP)

else:
    print('Drone1 with IP: %s returned an error' %droneIP)