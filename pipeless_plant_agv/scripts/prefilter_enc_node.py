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

# Global variables     



def main():
    # Configuration of the ros node stuff
	rospy.init_node('prefilter_enc')    
	pub = rospy.Publisher('encoder', encoder_data, queue_size=10)
	rate = rospy.Rate(4) # 4hz 
    	
	
	count1 = 0
	count2 = 0

	# Stuff for txt file aka. publisher
	pu_Delta= " "
	pu_Alpha = ' '
	num_ts1 = 4		#number of bytes which contain trash of  AGS=
	num_ts2 = 3		#number of bytes which contain trash of  ID=
	num_ID = 4		#number of bytes which contain the ID
	num_ts3 = 4		#number of bytes which contain trash of  SSI=
	num_ts4 = 2		#number of bytes which contain trash of  X/
	
	# Create instances of rfid_data
	enc_str = encoder_data()

	while not rospy.is_shutdown():
		# RFID init
		enc_str.delta = 0
		enc_str.alpha = 0
		# Request for sensor data Delta
		ser.write(chr(142))
		ser.write(chr(19))
		time.sleep(0.05)
		if ser.inWaiting() > 0:
			print("Encoder Delta")
			while ser.inWaiting() > 0:
				response = struct.unpack(">h",ser.read(2))[0]
				#v1 = response.decode('utf-8')
				enc_str.delta = response
				print(response)

		# Request for sensor data Alpha
		data = chr(142)
		ser.write(data)
		data =  chr(20)
		ser.write(data)
		time.sleep(0.05)
		if ser.inWaiting() > 0:
			#print("Encoder Alpha")
			while ser.inWaiting() > 0:
				response = struct.unpack(">h",ser.read(2))[0]
				#v1 = response.decode('utf-8')
				enc_str.alpha = response
		time.sleep(0.15)
		turning_speed = 54
		forward_speed = 100
		# Coordinate the motion
            	if count1==0:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(forward_speed))
		
			ser.write(chr(128))
			ser.write(chr(0))

		elif count1 ==30:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(turning_speed))
		
			ser.write(chr(0))
			ser.write(chr(0))
		elif count1==45:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(forward_speed))
		
			ser.write(chr(128))
			ser.write(chr(0))

		elif count1 ==60:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(turning_speed))
		
			ser.write(chr(0))
			ser.write(chr(0))

		elif count1==75:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(forward_speed))
		
			ser.write(chr(128))
			ser.write(chr(0))

		elif count1 ==105:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(turning_speed))
		
			ser.write(chr(0))
			ser.write(chr(0))
		elif count1==120:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(forward_speed))
		
			ser.write(chr(128))
			ser.write(chr(0))

		elif count1 ==137:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(turning_speed))
		
			ser.write(chr(0))
			ser.write(chr(0))

		# Stop the robot
		elif count1 ==153:
			ser.write(chr(137))

			ser.write(chr(0))
			ser.write(chr(0))

			ser.write(chr(128))
			ser.write(chr(0))

		count1 += 1
		# Publishing
		enc_str.header.stamp = rospy.Time.now()

		pub.publish(enc_str)
		#rate.sleep()
if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyAMA0', 57600)
	time.sleep(2)
	# Init of the AGV
	ser.write(chr(128))
	ser.write(chr(132))
	# Request for sensor data
	print("Request battery status")
	ser.write(chr(142))
	ser.write( chr(25))
	time.sleep(0.5)
	if ser.inWaiting() > 0:
		while ser.inWaiting() > 0:
			response = struct.unpack(">H",ser.read(2))[0]
			print response
	
	try:
		while not rospy.is_shutdown():
			main()
	except KeyboardInterrupt:
		print("Disconnected")
		ser.close()
