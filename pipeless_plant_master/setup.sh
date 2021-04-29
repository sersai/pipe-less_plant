#!/bin/bash
#TO RUN THIS BASH FILE $ bash setup.sh

#clear all working process'
sudo killall roscore
sudo killall rosmaster
kill -9
#start over
#gnome-terminal -- roscore

#python ~/catkin_ws/src/pipeless_plant_master/src/test.py
clear

rosrun pipeless_plant_master test.py

