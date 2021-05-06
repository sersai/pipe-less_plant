#!/usr/bin/env python
# license removed for brevity
import rospy
import serial
import time
def main():
	rate = rospy.Rate(4)
	if ser.inWaiting() > 0:
		ser.reset_input_buffer()
	while not rospy.is_shutdown():
		line = []
		if ser.inWaiting() > 0:
			while ser.inWaiting() > 0:
				for c in ser.read():
					line.append(c)
#				response = ser.read()
			print line
			print '####'
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
