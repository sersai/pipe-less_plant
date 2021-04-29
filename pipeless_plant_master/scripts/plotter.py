#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from pipeless_plant_master.msg import position
import numpy as np # We import numpy and rename it np (this is common practice)
import matplotlib.pyplot as plt # We import a module pyplot from the module matplotlib and rename it plt (again common practice)
import time, random,pylab

def positionCallback(data):
    global x,y
    x = data.x_pos
    y = data.y_pos
def visualization(i):
    global x,y

def main():
    global x,y
    rospy.init_node('plotter')    
    rate = rospy.Rate(4) # 4hz    
    i = 0 
    ####
    # fig,ax = plt.subplots()
    # ax.set_xlim((0,10))
    # ax.set_ylim((0,10))
    # plt.show()
    # time.sleep(3)
    # circle1 = plt.Circle((5,3),0.2)
    # ax.add_patch(circle1)
    # #plt.show()
    # ax.plot()
    # circle2 = plt.Circle((3,5),0.2)
    # ax.add_patch(circle2)
    # print "a"
    # time.sleep(3)
    # print "b"
    # ax.plot()
    # print "c"
    dat =[0,1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((0,10))
    ax.set_ylim((0,10))
    Ln, = ax.plot(dat)
    plt.ion()
    plt.show()
    # for i in range(10):
    #     dat.append(random.uniform(0,1))
    #     Ln.set_ydata(dat)
    #     Ln.set_xdata(range(len(dat)))
    #     if i is 3:
    #         print "here"
    #         circle1 = plt.Circle((5,3),0.2)
    #         ax.add_patch(circle1)
    #     if i is 5:
    #         print "here"
    #         circle1 = plt.Circle((3,5),0.2)
    #         ax.add_patch(circle1)
    #     plt.pause(0.1)
    ######
    while not rospy.is_shutdown(): 
    #     positionSub = rospy.Subscriber("/encoder", position, positionCallback)
        dat.append(random.uniform(0,1))
        Ln.set_ydata(dat)
        Ln.set_xdata(range(len(dat)))
        plt.pause(0.01)
        rate.sleep()

if __name__ == '__main__': 
    #pub = rospy.Publisher('location', position, queue_size=10)  
    main()