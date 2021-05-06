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
	testStr = ""
	rate = rospy.Rate(4)
	count = 0
	#
	empty_list = []
	print empty_list
	for i in range(0,255):
		empty_list.append('')
	#
	if ser.inWaiting() > 0:
		ser.reset_input_buffer()
	while not rospy.is_shutdown():
		testStr = ""
		if ser.inWaiting() > 0:
			collect = empty_list[:]
			while ser.inWaiting() > 0:
				test = ser.read_until('$')
				print test
#				response = ser.read()
#				if(response is '#'):
#					response = ser.read()
#					for i in range(1,int(response)+1):
#						test = ser.read_until(';')
#						print test
#					print("total number of tags: {}".format(int(response)+30))
#				testStr += response
#			print testStr
#			print '####'
		count = 0
		rate.sleep()
if __name__ == '__main__':
	rospy.init_node("test")
	ser = serial.Serial('/dev/ttyACM0', 115200)
	time.sleep(0.1)
	try:
		while not rospy.is_shutdown():
			main()
	except KeyboardInterrupt:
		print("Disconnected")
		ser.close()
