#This python script will run on the GS (Ground-Station)
#it will check to see if it can see any drones with the designated IP via PING
#and if the PING latency is below 200ms (arbitrarily chosen, should test to determine appropriate threshold)
#it will then initiate an rsync transfer of pictures stored in ~/Python/images to the machine's desktop
#TODO - implement handshake between pi and GS to confirm transfer of files is complete
#TODO - perhaps do files one at a time instead of a massive dump, or create archives... need to test best method of delivery

import os
import subprocess

#setup some variables
currDir = os.getcwd()
gsIP = '1.4.19.107' #needs to be updated to actual GS IP, probably of the 192.168.1.x variety
droneIP = '1.4.19.115' #needs to be updated to actual drone IP, probably of the 192.168.1.x variety, and in a list of several drones

#ping the bastard and see if it's available
p = subprocess.Popen(['ping', '-c', '3', droneIP], stdout=subprocess.PIPE)
output = p.communicate()
print output
rc = p.returncode
if rc == 0:
    print('%s active' % droneIP)

    #grab average ping
    print output.splitlines()[4]


elif rc == 2:
    print('%s no response' % droneIP)

else:
    print('%s error' %droneIP)

