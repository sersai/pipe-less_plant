#!/bin/bash
#TO RUN THIS BASH FILE $ bash setup.sh

#clear all working process'
#sudo killall roscore
#sudo killall rosmaster
#kill -9
#start over
gnome-terminal -- roscore

#rosrun pipeless_plant_master test.py
roslaunch pipeless_plant_master master.launch
