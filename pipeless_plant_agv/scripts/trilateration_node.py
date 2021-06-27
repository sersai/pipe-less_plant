#!/usr/bin/env python


import rospy
import fnc_trilateration_node as fnc_tri
from std_msgs.msg import String
from pipeless_plant_agv.msg import rfid_data
from pipeless_plant_agv.msg import position
#from pipeless_plant_master.msg import encoder_data
# Global variables
dist_be_tags = 140             # unit = mm
data_old = []
position_old = position()
position_old.x_pos = 0
position_old.y_pos = 0
delta = 1
#
def callback_temp(data):
    global delta
    delta = data.delta
#
def callback(data):
    global data_old
    global position_old
    global delta
#
    position_pub = position()
    #hello_str = data    # just for testing perposes
    if data_old!=data:
        delta = 0 #for testing without robot heading sensor
        position_pub = fnc_tri.esti_pos(data,position_old,dist_be_tags,delta)
        position_pub.header.stamp = rospy.Time.now()
        pub.publish(position_pub)

        data_old = data
        position_old = position_pub
#
def main():
    rospy.init_node('trilateration')
    #sub_enc = rospy.Subscriber("/encoder", encoder_data, callback_temp)
    sub = rospy.Subscriber("/rfid_reader_agv1", rfid_data, callback)
    rate = rospy.Rate(4)
    while not rospy.is_shutdown():
	rate.sleep()
#
if __name__ == '__main__': 
    pub = rospy.Publisher('location_agv1',position,queue_size=10)
    main()
