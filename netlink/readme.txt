these files are a smarter version of the network trasfer files. 
The drone side bradcasts UDP information for setting up a tcp link
that is used to do the actual file trasfer. The server side listens to
these broadcasts and starts a thread for every incoming drone connection
to handle the incoming files. 
