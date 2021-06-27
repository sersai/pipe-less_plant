#!/usr/bin/env python
import rospy, os, json, math
from pipeless_plant_master.msg import position

def callback(data):
    print data
def main ():
    rospy.init_node('test')
    sub = rospy.Subscriber("/location_agv1",position,callback)
    rate = rospy.Rate(4)
	
    while not rospy.is_shutdown():
#   	position_data = position()
#	print position_data
        rate.sleep()

if __name__ == '__main__':  
    main()
