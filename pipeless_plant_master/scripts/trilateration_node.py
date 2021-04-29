#!/usr/bin/env python


import rospy
import fnc_trilateration_node as fnc_tri
from std_msgs.msg import String
from pipeless_plant_master.msg import rfid_data
from pipeless_plant_master.msg import position
from pipeless_plant_master.msg import encoder_data

# Global variables
dist_be_tags = 140             # unit = mm
data_old = []
position_old = position()
position_old.x_pos = 0
position_old.y_pos = 0
delta = 1

def callback_temp(data):
    global delta
    delta = data.delta

def callback(data):
    global data_old
    global position_old
    global delta

    position_pub = position()
    #hello_str = data    # just for testing perposes
    if data_old!=data:
        print "$$$$$$$$$$"
        # Code done with the data 
        print "TAG1:{},{}   TAG2:{},{}  TAG3:{},{}  TAG4:{},{}".format(data.id1,data.rssi1,data.id2,data.rssi2,data.id3,data.rssi3,data.id4,data.rssi4)
        try:
            position_pub = fnc_tri.esti_pos(data,position_old,dist_be_tags,delta)
        except:
            print data
        # Done with the code
        position_pub.header.stamp = rospy.Time.now()
        pub.publish(position_pub)
        print "x:{},y:{},#:{}".format(position_pub.x_pos,position_pub.y_pos,data.number)
        print "###########"
        data_old = data
        position_old = position_pub

def main():
    rospy.init_node('trilateration')    
    sub_enc = rospy.Subscriber("/encoder", encoder_data, callback_temp) 
    sub = rospy.Subscriber("/rfid_reader_agv1", rfid_data, callback)   
    rate = rospy.Rate(4) # 4hz     
    while not rospy.is_shutdown():      
        rate.sleep()
    
if __name__ == '__main__': 
    pub = rospy.Publisher('location', position, queue_size=10)  
    main()
