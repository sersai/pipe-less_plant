import rospy
import pipeless_plant_agv.msg import rfid_data

def callback(data):
	print(data)

def main():
	rospy.init_node('obs')
	rate = rospy.Rate(4)
	sub = rospy.Subscriber("/rfid_reader", rfid_data, callback)
	while not rospy.is_shutdown():
		rate.sleep()

if __name__ == '__main__':
	try:
		while not rospy.is_shutdown():
			main()
	except KeyboardInterrupt:
		print "dc"
