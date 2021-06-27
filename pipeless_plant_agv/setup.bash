#
#Variables
#
#master_ip='192.168.0.86' #at home
#agv_ip='192.168.0.134' #at home
#master_ip='192.168.0.107' #at lab
#agv_ip='192.168.0.100' #at lab

master_ip='192.168.0.106'
agv_ip='192.168.0.100'
#
#end of variables
#
#
# do not change here, setup is automated to do:
#

export ROS_MASTER_URI=http://$master_ip:11311
export ROS_HOSTNAME=$agv_ip

roslaunch pipeless_plant_agv AGV.launch
