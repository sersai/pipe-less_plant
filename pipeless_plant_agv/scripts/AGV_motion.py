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
	global motion_type
	if motion_type is not type:
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
		print("command2 sent")
def main():
    # Configuration of the ros node stuff
	rospy.init_node('prefilter_enc') #initialize the ros node
	pub = rospy.Publisher('encoder', encoder_data, queue_size=10) #initialize ros topic encoder with ros msg encoder_data
	rate = rospy.Rate(10) # 4hz

	pu_Delta= ' '
	pu_Alpha = ' '
	straight = 32767
	turn = -1
	# Create instances of encoder_data
	enc_str = encoder_data()
	t = time.time()
	#ser.write(chr(157))
	#ser.write(chr(0))
	#ser.write(chr(90))
	while not rospy.is_shutdown():
		# RFID init
		enc_str.delta = 0
		enc_str.alpha = 0
		# Request for sensor data Delta
		ser.write(chr(142))
		ser.write(chr(19))
		time.sleep(0.05)
		if ser.inWaiting() > 0:
			while ser.inWaiting() > 0:
				response = struct.unpack(">h",ser.read(2))[0]
				#v1 = response.decode('utf-8')
				enc_str.delta = response
#				print("Encoder Delta: {}".format(response))
		# Request for sensor data Alpha
		data = chr(142)
		ser.write(data)
		data =  chr(20)
		ser.write(data)
		time.sleep(0.05)
		if ser.inWaiting() > 0:
			while ser.inWaiting() > 0:
				response = struct.unpack(">h",ser.read(2))[0]
				#v1 = response.decode('utf-8')
				enc_str.alpha = response
		time.sleep(0.15)
		# Coordinate the motion
		#current motion: [0-30) forward,[30-60) rotate, [60,~) stop
		range1 = 10
		range2 = 2
		range3 = 3
		range4 = 4
		# old
		# forward: 0 100 128 0 = 100
		# turning: 0 54 0 0 = 54
		# turning: 255 202 0 0= -54
		#backward: 255 156 128 0 = -100
		# new
		# forward/backward: (velocity[mm/s],32767)
		# turning: (velocity,-1)
		try:
			#AGV_motors2(100,200,1)
			if 0 <= time.time()-t < range1:
				#AGV_motors(255,156,128,0,1)
				AGV_motors2(100,200,1)
			elif range1 <= time.time()-t < range2:
				#AGV_motors(0,100,128,0,2)
				AGV_motors2(100,straight,2)
			elif range2 <= time.time()-t < range3:
				AGV_motors2(0,0,3)
			#	AGV_motors2(54,turn,3)
			elif range3 <= time.time()-t < range4:
				AGV_motors2(-100,straight,4)
			#	AGV_motors2(-54,turn,4)
			else:
				#AGV_motors2(0,0,5)
				t = time.time()
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
			AGV_motors2(0,0,98)
	except KeyboardInterrupt:
		print("Disconnected")
		AGV_motors2(0,0,99)
		ser.close()
