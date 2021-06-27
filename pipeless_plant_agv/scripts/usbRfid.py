#!/usr/bin/env python
# license removed for brevity
import rospy
import os
import serial
import time
#
from std_msgs.msg import String
from std_msgs.msg import UInt8
from pipeless_plant_agv.msg import rfid_data
# Global variables
empty_list = []
#
for i in range(0,255):
	empty_list.append('')
#
def RFID():
	global empty_list
	ser.write("AT+Inventory\r")
	time.sleep(0.25)
	if ser.inWaiting > 0:
		collect = empty_list[:]
		#print collect
		count = 0
		while ser.inWaiting() > 0:
			data = ser.read()
			collect[count] = data
			count += 1
		msg = filter(lambda x : x != '', collect)
		return msg
	return ""
#
def msgF(msgIn,in1,in2):
	msg = msgIn + "|"+str(in1)+"-"+str(in2)+"|"
	return msg
def main():
	rospy.init_node('prefilter1')
	pub = rospy.Publisher('rfid_reader_agv1',rfid_data, queue_size = 10)
	rate = rospy.Rate(4)
	rate.sleep()
	if ser.inWaiting() > 0:
		ser.reset_input_buffer()
	ser.write("AT+Scan=OFF\r")
	rate.sleep()
	thrash = RFID()
	rate.sleep()
	while not rospy.is_shutdown():
		rfid_str = rfid_data()
		try:
			msg = RFID()
			if  msg:
				nTags = int(msg[6])
				rfid_str.number = nTags
				showMsg = str(rfid_str.number)
				if nTags is 1 or nTags > 1:
					tempMsg = msg[8:40]
					rfid_str.id1 = "".join(tempMsg[17:21]) # msg[13:29]
					rfid_str.rssi1 = int(tempMsg[28])
					showMsg = msgF(showMsg,rfid_str.id1,rfid_str.rssi1)
				if nTags is 2 or nTags > 2:
					tempMsg = msg[40:72]
					rfid_str.id2 = "".join(tempMsg[17:21])
					rfid_str.rssi2 = int(tempMsg[28])
					showMsg = msgF(showMsg,rfid_str.id2,rfid_str.rssi2)
				if nTags is 3 or nTags > 3:
					tempMsg = msg[72:104]
					rfid_str.id3 = "".join(tempMsg[17:21])
					rfid_str.rssi3 = int(tempMsg[28])
					showMsg = msgF(showMsg,rfid_str.id3,rfid_str.rssi3)
				if nTags is 4 or nTags > 4:
					tempMsg = msg[104:136]
					rfid_str.id4 = "".join(tempMsg[17:21])
					rfid_str.rssi4 = int(tempMsg[28])
					showMsg = msgF(showMsg,rfid_str.id4,rfid_str.rssi4)
				if nTags is 5:
					tempMsg = msg[136:168]
					rfid_str.id5 = "".join(tempMsg[17:21])
					rfid_str.rssi5 = int(tempMsg[28])
					showMsg = msgF(showMsg,rfid_str.id5,rfid_str.rssi5)
			else:
				rfid_str.number = 98
		except Exception as e:
			print e
			rfid_str.number = 99
#		print showMsg
		rfid_str.header.stamp = rospy.Time.now()
		pub.publish(rfid_str)
#
if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0', 115200)
	time.sleep(0.1)
	try:
		while not rospy.is_shutdown():
			main()
	except KeyboardInterrupt:
		print("Disconnected")
		ser.close()
