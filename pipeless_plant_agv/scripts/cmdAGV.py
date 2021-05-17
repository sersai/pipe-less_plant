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
def requestDelta():
	ser.write(chr(142))
	ser.write(chr(19))
	time.sleep(0.05)
	if ser.inWaiting() > 0:
		while ser.inWaiting() > 0:
			d = struct.unpack(">h",ser.read(2))[0]
	else:
		d = 0
	return d
def requestAlpha():
	ser.write(chr(142))
	ser.write(chr(20))
	time.sleep(0.05)
	if ser.inWaiting() > 0:
		while ser.inWaiting() > 0:
			a = struct.unpack(">h",ser.read(2))[0]
	else:
		a = 0
	return a

def AGV_motors2(velocity,radius,goal):
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
	thrash = requestDelta()
	delta = 0
	while delta <= goal:
		deltaTemp = requestDelta()
		delta += deltaTemp
		print delta
	print delta
	ser.write(chr(137))
	ser.write(chr(0))
	ser.write(chr(0))
	ser.write(chr(0))
	ser.write(chr(0))

def main():
	global tf
	# Configuration of the ros node stuff
	rospy.init_node('prefilter_enc') #initialize the ros node
	pub = rospy.Publisher('encoder', encoder_data, queue_size=10) #initialize ros topic encoder with ros msg encoder_data
	rate = rospy.Rate(10) # 4hz

	straight = 32767
	turn = -1
	# Create instances of encoder_data
	try:
		print "turn0"
		AGV_motors2(0,0,0)
		#AGV_motors2(100,straight,500)
		print "turn1"
	except Exception as e:
		print "error on AGV_motors function"
		print e
		AGV_motors2(0,0,0)

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
		print "main0"
		main()
		print "main1"
		AGV_motors2(0,0,0)
	except KeyboardInterrupt:
		print("Disconnected")
		AGV_motors2(0,0,0)
		ser.close()
