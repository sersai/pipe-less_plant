#!/usr/bin/env python
import rospy, sys, time
from pipeless_plant_master.msg import rfid_data

def callback(data):
	print data

def main():
	rospy.init_node('master')   
	sub_rfid = rospy.Subscriber("/rfid_reader", rfid_data, callback) 
	rate = rospy.Rate(4) # 4hz   


 	while not rospy.is_shutdown(): 
 		rate.sleep()

if __name__ == '__main__':
	time.sleep(0.1)
	try:
		main()
	except rospy.ROSInterruptException:
		rospy.loginfo("Program terminated.")