#!/usr/bin/env python
# license removed for brevity
import rospy
import os
import serial
import time
import struct

from std_msgs.msg import String
from std_msgs.msg import UInt8
#from pipeless_plant_agv.msg import rfid_data
from pipeless_plant_agv.msg import encoder_data

def main():
    # Configuration of the ros node stuff
	rospy.init_node('prefilter_enc')
	pub = rospy.Publisher('encoder', encoder_data, queue_size=10)
	rate = rospy.Rate(4) # 4hz

	count1 = 0

	enc_str = encoder_data()

	while not rospy.is_shutdown():
		enc_str.delta = count1
		enc_str.alpha = count1*2
		count1 += 1
		enc_str.header.stamp = rospy.Time.now()
		pub.publish(enc_str)
		rate.sleep()
if __name__ == '__main__':
	try:
		while not rospy.is_shutdown():
			main()
	except KeyboardInterrupt:
		print("Disconnected")
