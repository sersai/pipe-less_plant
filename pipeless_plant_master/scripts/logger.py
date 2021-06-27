#!/usr/bin/env python
# license removed for brevity
import rospy,time
import os

from std_msgs.msg import String
from std_msgs.msg import UInt8
from pipeless_plant_master.msg import rfid_data
from pipeless_plant_master.msg import position
from pipeless_plant_master.msg import encoder_data
from pipeless_plant_master.msg import experiment
rfid = rfid_data()
location = position()
experimentMsg = experiment()
def location_callback(data):
    global location
    location = data
def rfid_callback(data):
    global rfid
    rfid = data
def experiment_callback(data):
    global experimentMsg
    experimentMsg = data
def main():
    global rfid,location,experimentMsg
    # Configuration of the ros node stuff
    rospy.init_node('logger_node')    
    timeStart = rospy.get_time()
    sub = rospy.Subscriber("/rfid_reader_agv1", rfid_data, rfid_callback)  
    sub = rospy.Subscriber("/location_agv1", position, location_callback)  
    sub = rospy.Subscriber("/experiment_agv1",experiment,experiment_callback)
    rate = rospy.Rate(4) # 4hz

    while not rospy.is_shutdown(): 
       	while not experimentMsg.start:
	    if rospy.is_shutdown():
		break
	if rospy.is_shutdown():
            break
    # create new experiment log file in every new run
        fileVal = 1
        script_dir = os.path.dirname(__file__)
        rel_path = "experiment_"+str(fileVal)+".txt"
        abs_file_path = os.path.join(script_dir, rel_path)
        while os.path.isfile(abs_file_path):
            fileVal += 1
            rel_path = "experiment_"+str(fileVal)+".txt"
            abs_file_path = os.path.join(script_dir, rel_path)
	print "experiment "+str(fileVal)+" started"
    #
        while not rospy.is_shutdown(): 
            #clean log data
            logData = ""
            #add rfid data to log
            logData = str(rfid.number)+','+ str(rfid.id1)+','+ str(rfid.rssi1)+','+ str(rfid.id2)+','+ str(rfid.rssi2)+','+ str(rfid.id3)+','+ str(rfid.rssi3)+','+ str(rfid.id4)+','+ str(rfid.rssi4)+','+ str(rfid.id5)+','+ str(rfid.rssi5)+','
        #add location data to log
            logData += str(location.x_pos)+','+str(location.y_pos)+','+str(location.fault)+','
        #add time to log
            timeNow = rospy.get_time() -timeStart
            logData += str(timeNow)+'\r'
        # rfid.header.stamp.to_sec()-timeStart
        # location.header.stamp.to_sec()-timeStart      
            with open(abs_file_path, 'a') as file_object:
                file_object.write(logData)
	    if not experimentMsg.start:
		break
            rate.sleep()
	print "experiment "+str(fileVal)+" done"
    
if __name__ == '__main__':
    try:
        print"logger node begins!"
        main()
    except KeyboardInterrupt:
        print("closing logger")

