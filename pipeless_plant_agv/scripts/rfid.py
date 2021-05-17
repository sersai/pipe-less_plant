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
	rospy.init_node('prefilter1')
	pub = rospy.Publisher('rfid_reader_agv1',rfid_data, queue_size = 10)
	rate = rospy.Rate(4)
	rate.sleep()
	if ser.inWaiting() > 0:
		ser.reset_input_buffer()
#	rfid_str = rfid_data()

	while not rospy.is_shutdown():
		rfid_str = rfid_data()
		try:
			if ser.inWaiting() > 0:
				while ser.inWaiting() > 0:
					data = ser.read_until('$')
					if ser.inWaiting() > 0:
						ser.reset_input_buffer()
				splitData = data.split(';')
				try:
					nTags = int(splitData[0])
				except:
					nTags = 0
				rfid_str.number = nTags
				if nTags is 1 or nTags > 1:
					rfid_str.id1 = splitData[1]
					rfid_str.rssi1 = int(splitData[2])
				if nTags is 2 or nTags > 2:
					rfid_str.id2 = splitData[3]
					rfid_str.rssi2 = int(splitData[4])
				if nTags is 3 or nTags > 3:
					rfid_str.id3 = splitData[5]
					rfid_str.rssi3 = int(splitData[6])
				if nTags is 4 or nTags > 4:
					rfid_str.id4 = splitData[7]
					rfid_str.rssi4 = int(splitData[8])
				if nTags is 5:
					rfid_str.id5 = splitData[9]
					rfid_str.rssi5 = int(splitData[10])
#				print rfid_str
#				print splitData
		except:
			rfid_str.number = 99
#		print rfid_str
		rfid_str.header.stamp = rospy.Time.now()
		pub.publish(rfid_str)
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
