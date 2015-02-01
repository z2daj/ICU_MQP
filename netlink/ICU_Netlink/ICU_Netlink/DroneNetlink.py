import sys
import time
from socket import *

print "starting up drone module"

#Define the port that the ground station will be listening on.
gsListenPort = 5005 
gsConnected = False

#setup the TCP server
tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.bind(('', 0)) #allow the system to find the best network ip and socket
tcpServer.listen(1)
#set the blocking to none so that we can loop while waiting for UDP to find a client
tcpServer.setblocking(0) 

tcpIncomingSocket = tcpServer.getsockname()[1]

#start the UDP broadcast
sock = socket(AF_INET, SOCK_DGRAM) 
sock.bind(('', 0))
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

#loop until a connection is recived over tcp
print "waiting for incoming connection"
trys = 0
while not gsConnected:
    sock.sendto(str(tcpIncomingSocket), ('<broadcast>', gsListenPort))
    time.sleep(1)

    try:
        conn, address = tcpServer.accept()
    except:
        print "no connection for loop: ", trys
    else:
        gsConnected = True
    trys = trys + 1
    
#we have a connection, go into tx mode
tcpServer.setblocking(1) 
while True:
    conn.send(time.asctime())
    time.sleep(1)

conn.close()
    
