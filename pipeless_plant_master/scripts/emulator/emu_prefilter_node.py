#!/usr/bin/env python
# license removed for brevity
#this script has the sole purpose of acting as a testing node to act like reading data from RFID module and encoder
import rospy
import os

from std_msgs.msg import String
from std_msgs.msg import UInt8
from pipeless_plant_master.msg import rfid_data
from pipeless_plant_master.msg import encoder_data

def main():
    # Configuration of the ros node stuff
    rospy.init_node('prefilter')    
    pub = rospy.Publisher('rfid_reader_agv1', rfid_data, queue_size=10)
    pub_enc = rospy.Publisher('encoder', encoder_data, queue_size=10)
    rate = rospy.Rate(4) # 4hz
    
    # Writing text is not good 'bla.txt'
    script_dir = os.path.dirname(__file__)
    rel_path = "Meas_desktop12.txt"
    rel_path2 = "Encoder.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    abs_file_path2 = os.path.join(script_dir, rel_path2)
    # Open RFID information from Emulator    
    file = open(abs_file_path, 'r')
    txt_data = file.readlines(2)   # txt_data contains the whole textfile
    file.close()
    # Open Encoder information from Emulator 
    file = open(abs_file_path2, 'r')
    txt_data2 = file.readlines(2)   # txt_data contains the whole textfile
    file.close()
    rate.sleep()
    size_file = len(txt_data) # = 348 at the moment
    gl_count = 0
    gl_count2 = 0
    # Create instances of rfid_data and encoder_data
    rfid_str = rfid_data()
    encoder_str = encoder_data()
    while not rospy.is_shutdown(): 
        # RFID information
        # sample for MEas_desktop10.txt, parantesis for each step has an example of parsing the RFID data series,
        # 4
        # DCEB       0
        # D75A       6
        # E757       0
        # D992       0
        # 3
        # D75A       6
        # E757       0
        # D992       0
        step = int(txt_data[gl_count]) #reads the total number of tags from RFID (step = 4 for gl_count = 0,step = 3 for gl_count = 5 = step+gl_count+1)
        rfid_str.number = step #save the total number of IDs to ros msg (rfid_str.number = 4)
        id_list = ["0000","0000","0000","0000","0000"] #set a list of IDs, at max 5 for the current setup
        rssi_list = [0, 0, 0, 0, 0] #set a list of RSSI values, at max 5 for the current setup
        # Split the string for rfid data 
        for x in range(gl_count,gl_count+step): # loop from the current till the end of tags of each data series ( x = from gl_count = 0 to gl_count+step = 0+4) 
            temp = txt_data[x+1].split() # save the current+1 into temp as a list with two elements temp[0]= tag id, temp[1] = RSSI value of that tag, (x=0 temp ='DCEB','0'],x=1 temp= ['DCEB', '0'],x=2 temp=['E757','0'],x=3 temp=['D992','0']) 
            id_list[x-gl_count] = temp[0] # save the that id to id_list, (x=0 id_list[0]=id_list[0-0]=temp[0]=DCEB, x=1 id_list[1]=id_list[1-0]=temp[0]=D75A, and so on)
            rssi_list[x-gl_count] = int(temp[1]) #save the respective RSSI value to rssi_list, ((x=0 rssi_list[0]=rssi_list[0-0]=temp[1]=0, x=1 rssi_list[1]=rssi_list[1-0]=temp[1]=6, and so on))
        #save all rfid tag ids and RSSI values to ros msg
        rfid_str.id1 = id_list[0]
        rfid_str.id2 = id_list[1]
        rfid_str.id3 = id_list[2]
        rfid_str.id4 = id_list[3]
        rfid_str.id5 = id_list[4]
        
        rfid_str.rssi1 = rssi_list[0]
        rfid_str.rssi2 = rssi_list[1]
        rfid_str.rssi3 = rssi_list[2]
        rfid_str.rssi4 = rssi_list[3]
        rfid_str.rssi5 = rssi_list[4]
        # Encoder information
        #sample for Encoder.txt,
        # 0,   0
        # 13,   0
        # 21,   0
        # 22,   0
        # Split the string for rfid data       
        temp2 = txt_data2[gl_count2].split(',')    #seperate each line of encoder data by "," marker,(x=0 temp2=['0', '0\n'],x=1 temp2=['13','0\n']
        #save current encoder data to ros msg     
        encoder_str.delta = int(temp2[0])
        encoder_str.alpha = int(temp2[1])
        
        #since we have read the current rfid data, need to jump to next data in simulation, 
        #which means in the text file gl_count must show next total number of tags
        #new indicator found from current indicator + total number of previous data + 1 
        gl_count = gl_count + step + 1 
        #same process for encoder but easier since next encoder data can basically be read from next line on the text
        gl_count2 += 1
        #since this script is just a simulation there is an end to the pre-recorded data.
        #Once this point is reached simulation will repeat from the beginning by resetting the counters
        if gl_count >= size_file:
            gl_count = 0
            gl_count2 = 0
        
        # Publishing
        rfid_str.header.stamp = rospy.Time.now()
        encoder_str.header.stamp = rospy.Time.now()

        pub.publish(rfid_str)
        pub_enc.publish(encoder_str)      
        
        rate.sleep()
    
if __name__ == '__main__':
    main()
