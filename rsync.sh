#!/usr/bin/expect

#this script will run rsync to pull data from a remote drone
#TODO - make it expandable -> i.e. any IP address can be fed into the script instead of having a single hardcoded value

spawn rsync -avz pi@1.4.19.115:~/Python/images ~/Desktop
expect "pi@1.4.19.115's password:"
send "raspberry\n"
interact