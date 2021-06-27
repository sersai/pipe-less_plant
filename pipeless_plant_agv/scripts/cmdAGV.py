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
from pipeless_plant_agv.msg import experiment
#
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
#
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
#
def straight(velocity,goal):
	highVelocity,lowVelocity = struct.pack('>h',velocity)
	highVelocity = int(highVelocity.encode('hex'), 16)
	lowVelocity = int(lowVelocity.encode('hex'), 16)
	thrash = requestAlpha()
	thrash = requestDelta()
#	print thrash
	ser.write(chr(137))
	ser.write(chr(highVelocity))
	ser.write(chr(lowVelocity))
	ser.write(chr(128))
	ser.write(chr(0))
	delta = 0
	if velocity > 0:
		while delta < goal:
			deltaTemp = requestDelta()
			delta += deltaTemp
	elif velocity < 0:
		while delta  > -goal:
			deltaTemp = requestDelta()
			delta += deltaTemp
	motors(0,0,0,0)
#	print "delta endocer:{}".format(delta)
# positive goal turns the AGV to left
# negative goal turn the aGV to right
def turn(goal):
	if goal > 0:
		v1 = 1
		v2 = 144 #54
	else:
		v1 = 255 #255
		v2 = 136 #202
	thrash = requestAlpha()
	thrash = requestDelta()
	ser.write(chr(137))
	ser.write(chr(v1))
	ser.write(chr(v2))
	ser.write(chr(0))
	ser.write(chr(0))
	alpha = 0
	if goal > 0:
		while alpha < goal:
			alphaTemp = requestAlpha()
			alpha += alphaTemp
	elif goal < 0:
		while alpha > goal:
			alphaTemp = requestAlpha()
			alpha += alphaTemp
	motors(0,0,0,0)
#	print "alpha encoder:{}".format(alpha)
def motors(val1,val2,val3,val4):
	ser.write(chr(137))
	ser.write(chr(val1))
	ser.write(chr(val2))
	ser.write(chr(val3))
	ser.write(chr(val4))
def loop1(): # square path
	angle = 90
	for i in range(4):
		straight(500,500)
		time.sleep(1)
		turn(angle)
		time.sleep(1)
def move(velocity, radius, goal):
	alpha = requestAlpha()
	totalAlpha = 0
	#
	hiVel,loVel = struct.pack('>h',velocity)
	hiRad,loRad = struct.pack('>h',radius)
	hiVel = int(hiVel.encode('hex'),16)
	loVel = int(loVel.encode('hex'),16)
	hiRad = int(hiRad.encode('hex'),16)
	loRad = int(loRad.encode('hex'),16)
	#print "velocity:{} hiVel:{} loVel:{} radius:{} hiRad:{} loRad:{}".format(velocity,hiVel,loVel,radius, hiRad,loRad)
	motors(hiVel,loVel,hiRad,loRad)
	#
	rate = rospy.Rate(10)
	while totalAlpha <= goal:
		alpha = requestAlpha()
		totalAlpha += abs(alpha)
		rate.sleep()
	motors(0,0,0,0)
def loop2(): # circular paths, move(velocity,radius,goal in angles)
	# version a
	#move(400,500,180)
	#move(400,-500,180)
	#move(400,-1000,180)
	# version b
	speed= 400
	radius = 200
	move(speed,radius,180)
	move(speed,-radius,360)
	move(speed,radius,180)
def main():
	global tf
	# Configuration of the ros node stuff
	rospy.init_node('prefilter_enc') #initialize the ros node
	pub = rospy.Publisher('encoder', encoder_data, queue_size=10) #initialize ros topic encoder with ros msg encoder_data
	pubExperiment = rospy.Publisher('experiment_agv1',experiment,queue_size=10)
	rate = rospy.Rate(10) # 4hz

	# Create instances of encoder_data
	time.sleep(1)
	try:
		experiment_pub = experiment()
		experiment_pub.start = True
		pubExperiment.publish(experiment_pub)
		print "loop begins"
		loop2()
		print "loop ends"
		experiment_pub = experiment()
		experiment_pub.start = False
		pubExperiment.publish(experiment_pub)
	except Exception as e:
		print "error on AGV_motors function"
		print e
		motors(0,0,0,0)

if __name__ == '__main__':
	print "main begins"
	ser = serial.Serial('/dev/ttyAMA0', 57600)
	time.sleep(2)
	# Init of the AGV
	ser.write(chr(128))
	ser.write(chr(132))
	#Request for sensor data
	print("Request battery status")
	ser.write(chr(142))
	ser.write( chr(25))
	time.sleep(0.5)
	if ser.inWaiting() > 0:
		while ser.inWaiting() > 0:
			response = struct.unpack(">H",ser.read(2))[0]
			print response
	try:
		main()
		motors(0,0,0,0)
#		ser.close()
		print "main ends"
	except KeyboardInterrupt:
		print("Disconnected")
		stop()
		ser.close()
