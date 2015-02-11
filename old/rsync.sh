#!/usr/bin/expect

#this script will run rsync to pull data from a remote drone
#TODO - make it expandable -> i.e. any IP address can be fed into the script instead of having a single hardcoded value

#echo "The drone IP is: "
spawn rsync -avz pi@1.4.19.175:~/Python/ICU_MQP/images /Users/Zach/Desktop
expect "pi@1.4.19.175's password:"
send "raspberry\n"
interact