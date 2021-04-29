#!/usr/bin/env python
# license removed for brevity
import rospy
import os
import serial
import time

from std_msgs.msg import String
from std_msgs.msg import UInt8
from pipeless_plant_agv.msg import rfid_data
# Global variables
#
def main():
	# Configuration of the ros node stuff
	rospy.init_node('prefilter') #initialize ros node with the name 'prefilter'
	pub = rospy.Publisher('rfid_reader_agv1', rfid_data, queue_size=10) #setup a new ros topic called 'rfid_reader_agv1' with ros msg rfid_data
	rate = rospy.Rate(4) #4hz
	rate.sleep()
	while not rospy.is_shutdown():
		dataStr = " "
		if ser.inWaiting() > 0:
			while ser.inWaiting() > 0:
				response  =  ser.read()
				print(response)
				dataStr += response
		print dataStr
		print "##################"
		rate.sleep()
if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', 115200)
	time.sleep(0.1)
	try:
		while not rospy.is_shutdown():
			main()
	except KeyboardInterrupt:
		print("Disconnected")
		ser.close()
