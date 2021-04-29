#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from pipeless_plant_master.msg import position
import numpy as np # We import numpy and rename it np (this is common practice)
import matplotlib.pyplot as plt # We import a module pyplot from the module matplotlib and rename it plt (again common practice)
import time, random,json, os

def positionCallback(data):
    global x,y
    x = data.x_pos
    y = data.y_pos
def main():
    global x,y
    x = 0
    y = 0
    rospy.init_node('plotter')    
    rate = rospy.Rate(4) # 4hz    
    ###### Plot Setup
    script_dir = os.path.dirname(__file__)
    rel_path1 = "IDPOS_small.txt"
    abs_file_path1 = os.path.join(script_dir, rel_path1)   
    # Load TagID - Pos List
    if os.path.isfile(abs_file_path1) == True:
        with open(abs_file_path1) as jason_file:
            POSID = np.array(json.load(jason_file))
    else:
        print("No txt-file for TagID to Position")  
    row,col = np.shape(POSID)
    dist_be_tags = 140
    #matplotlib.use('TkAgg')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((-50,col*dist_be_tags))
    ax.set_ylim((row*dist_be_tags,-50))
    plt.ion()
    plt.show()
    for i in range(row):
        for j in range(col):
	        circle1 = plt.Circle((j*dist_be_tags,i*dist_be_tags),10,color = 'b')
	        ax.add_patch(circle1)
    circle2 = plt.Circle((j*dist_be_tags,i*dist_be_tags),10,color = 'b')
    ax.add_patch(circle2)
    plt.pause(0.0001)
    ##### end of plot setup
    positionSub = rospy.Subscriber("/location", position, positionCallback)
    xOld = 0
    yOld = 0
    while not rospy.is_shutdown():
        if(xOld is not x and yOld is not y):
            circle2.remove()
            circle2 = plt.Circle((x,y),165,color = 'r', fill =False)
            ax.add_patch(circle2)
            plt.pause(0.0001)
            xOld = x
            yOld = y
            print(x,y)
            rate.sleep()

if __name__ == '__main__': 
    #pub = rospy.Publisher('location', position, queue_size=10)  
    main()
