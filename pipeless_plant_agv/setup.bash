#
#Variables
#
master_ip='192.168.0.86'
agv_ip='192.168.0.134'

#master_ip='192.168.0.106'
#agv_ip='192.168.0.100'
#
#end of variables
#
#
# do not change here, setup is automated to do:
#

export ROS_MASTER_URI=http://$master_ip:11311
export ROS_HOSTNAME=$agv_ip

roslaunch pipeless_plant_agv AGV.launch
#rosrun pipeless_plant_agv prefilter_node.py
