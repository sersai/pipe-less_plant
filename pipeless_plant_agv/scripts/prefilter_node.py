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
	gl_count = 0
	response = ' '
	str_ts1 = ' '
	str_ts2 = ' '
	str_ts3 = ' '
	# Stuff for txt file aka. publisher
	pu_number = ' '
	pu_ID = " "
	pu_RSSI = ' '
	num_ts1 = 4		#number of bytes which contain trash of  AGS=
	num_ts2 = 3		#number of bytes which contain trash of  ID=
	num_ID = 4		#number of bytes which contain the ID
	num_ts3 = 4		#number of bytes which contain trash of  SSI=
	num_ts4 = 2		#number of bytes which contain trash of  X/
	# Create instances of rfid_data
	rfid_str = rfid_data()

	while not rospy.is_shutdown():
		# RFID init
		rfid_str.number = 0
		rfid_str.id1 = "0000"
		rfid_str.id2 = "0000"
		rfid_str.id3 = "0000"
		rfid_str.id4 = "0000"
		rfid_str.id5 = "0000"

		rfid_str.rssi1 = 0
		rfid_str.rssi2 = 0
		rfid_str.rssi3 = 0
		rfid_str.rssi4 = 0
		rfid_str.rssi5 = 0
		# Recording RFID data, incoming data will look like:
		#+TAGS=0OK #no tag(s) read
		#+TAGS=1+UID=E00401503A5BD993,+RSSI+4/4OK # 1 tag read
		#+TAGS=2+UID=E00401503A5BD993,+RSSI+4/4+UID=E00401503A5BD992,+RSSI+3/3OK # 2 tags read
		#and the following while loop will parse the incoming character by character,
		#system basically looks for the characters
		#'T' from incoming data, if char='T', skip the next 4 chars='AGS=', read the following char = n #number of tags
		#'U' from incoming data, if char='U', skip the next 3 chars='ID=', tag ID has 16 bytes for our system we only care with last 4 bytes so the following 16 characters are seperated into two, first 12 bytes are thrash (don't care), last 4 bytes are saved under pu_ID
		#'R' from incoming data, if char='R', skip the next 4 chars='SSI+', read the following char = p # RSSI value of respective tag
		try:
			if ser.inWaiting() > 0:
				while ser.inWaiting() > 0:
					response  =  ser.read()
					# detecting the number of tags
					if response == 'T':
						gl_count = 0
						msg_ts1 = " "
						for i in range(0,num_ts1):
							str_ts1 = ser.read()
							msg_ts1 += str_ts1
						if msg_ts1 == " AGS=":
							pu_number = ser.read()
						rfid_str.number = int(pu_number)
					# detecting the ID
					elif response == 'U':
						gl_count += 1
						msg_ts2 = " "
						for i in range(0,num_ts2):
							str_ts2 = ser.read()
							msg_ts2 += str_ts2
						if msg_ts2 == " ID=":
							trash = ser.read(num_ts2*4)
							pu_ID = ser.read(num_ID)
						#Writing the IDs
						if gl_count == 1:
							rfid_str.id1 = pu_ID
						elif gl_count == 2:
							rfid_str.id2 = pu_ID
						elif gl_count == 3:
							rfid_str.id3 = pu_ID
						elif gl_count == 4:
							rfid_str.id4 = pu_ID
						elif gl_count == 5:
							rfid_str.id5 = pu_ID
				# detecting RSSI
					elif response == 'R':
						msg_ts3 = " "
						for i in range(0,num_ts3):
							str_ts3 = ser.read()
							msg_ts3 += str_ts3
						if msg_ts3 == " SSI=":
							trash = ser.read(num_ts4)
							pu_RSSI = ser.read()
						#Writing the RSSI
						if gl_count == 1:
							rfid_str.rssi1 = int(pu_RSSI)
						elif gl_count == 2:
							rfid_str.rssi2 = int(pu_RSSI)
						elif gl_count == 3:
							rfid_str.rssi3 = int(pu_RSSI)
						elif gl_count == 4:
							rfid_str.rssi4 = int(pu_RSSI)
						elif gl_count == 5:
							rfid_str.rssi5 = int(pu_RSSI)
		except:
			rfid_str.number = 99
			rfid_str.id1 = "0000"
			rfid_str.id2 = "0000"
			rfid_str.id3 = "0000"
			rfid_str.id4 = "0000"
			rfid_str.id5 = "0000"
			rfid_str.rssi1 = 0
			rfid_str.rssi2 = 0
			rfid_str.rssi3 = 0
			rfid_str.rssi4 = 0
			rfid_str.rssi5 = 0
		gl_count = 0
		# Publishing
		print rfid_str
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
