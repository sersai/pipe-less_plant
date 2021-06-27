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
motion_type = 0
def AGVturn(angle,type):
	global motion_type
	if motion_type is not type:
		print "turn"
		ser.write(chr(157))
		#ser.write(chr(0))
		ser.write(chr(angle))
def AGV_motors(value1, value2, value3, value4, type):
	global motion_type
	if motion_type is not type:
		motion_type = type
		ser.write(chr(137))
		ser.write(chr(value1))
		ser.write(chr(value2))
		ser.write(chr(value3))
		ser.write(chr(value4))
		print("command sent")
def AGV_motors2(velocity,radius,type):
	global motion_type, tf
	if motion_type is not type:
		ser.write(chr(142))
		ser.write(chr(19))
		time.sleep(0.05)
		if ser.inWaiting() > 0:
			while ser.inWaiting() > 0:
				delta = struct.unpack(">h",ser.read(2))[0]
		ser.write(chr(142))
		ser.write(chr(20))
		time.sleep(0.05)
		if ser.inWaiting() > 0:
			while ser.inWaiting() > 0:
				alpha = struct.unpack(">h",ser.read(2))[0]
		#
		motion_type=type
		highVelocity,lowVelocity = struct.pack('>h',velocity)
		highRadius,lowRadius = struct.pack('>h',radius)
		highVelocity = int(highVelocity.encode('hex'), 16)
		lowVelocity = int(lowVelocity.encode('hex'), 16)
		highRadius = int(highRadius.encode('hex'), 16)
		lowRadius = int(lowRadius.encode('hex'), 16)
		ser.write(chr(137))
		ser.write(chr(highVelocity))
		ser.write(chr(lowVelocity))
		ser.write(chr(highRadius))
		ser.write(chr(lowRadius))
		#print("command2 sent")
		print "t: {:.2f} delta:{} alpha:{}".format(time.time()-tf,delta,alpha)

def main():
	global tf
	# Configuration of the ros node stuff
	rospy.init_node('prefilter_enc') #initialize the ros node
	pub = rospy.Publisher('encoder', encoder_data, queue_size=10) #initialize ros topic encoder with ros msg encoder_data
	rate = rospy.Rate(10) # 4hz

	straight = 32767
	turn = -1
	# Create instances of encoder_data
	enc_str = encoder_data()
	t = time.time()
	tf = time.time()
	print "entering loop"
#	ser.write(chr(157))
#	ser.write(chr(0))
#	ser.write(chr(90))
#	AGV_motors2(100,straight,1)
	while not rospy.is_shutdown():
		# RFID init
		enc_str.delta = 0
		enc_str.alpha = 0
		time.sleep(0.15)
		range1 = 5
		try:
			if 0<= time.time()-t < range1:
				AGV_motors2(100,straight,1)
		#	elif range1 <= time.time()-t < 10:
		#		AGV_motors2(100,straight,2)
			else:
				AGV_motors2(0,0,2)
#				t = time.time()
		except Exception as e:
			print "error on AGV_motors function"
			print e
			AGV_motors(0,0,0,0,99)
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
			AGV_motors(0,0,0,0,98)
	except KeyboardInterrupt:
		print("Disconnected")
		AGV_motors(0,0,0,0,99)
		ser.close()
