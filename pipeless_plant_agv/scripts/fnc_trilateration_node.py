# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 17:57:21 2019

@author: stephan
"""
#TODO
# read the bilateration and trilateration again,
# no error on 2 tags (might be happening because there aren't many or any 2 tag data) but 3-4-5 tags raises errors
# first add a description of calculations for bilateration_two function
# then solve problems on 3,4 and 5 tags in this order.
import json
import os
import math
import rospy
#
##
#
from pipeless_plant_master.msg import rfid_data
from pipeless_plant_master.msg import position
#
## function: dist_ptp
#
## INPUT VARIABLES
#p1: position of first tag, p1 = [position in x direction (x1), position in y direction (y1)]
#p2: position of second tag, p2 = [position in x direction (x2), position in y direction (y2)]
## OUTPUT VARIABLE
#dist: distance between two tags, dist = sqrt((y2-y1)^2+(x2-x1)^2)
##
#
def dist_ptp(p1,p2):
    try:
        dist = math.sqrt((p2[1]-p1[1])**2+(p2[0]-p1[0])**2)
        return dist
    except Exception as e:
        print "error in dist_ptp function on fnc_trilateration_node.py"
        print e
    
#
## function: find_array
#
## INPUT VARIABLES
#POSID: data set of mapped IDs on the plant floor (consider POSID data set as a matrix of tag IDs)
#ID: one of the tag ID read by RFID module
#dist_be_tags: distance between passive tags in the system (currently 140 mm)
## OUTPUT VARIABLE
#tag: position of the tag in the system, tag = [position in x direction, position in y direction]
## FUNCTION DESCRIPTION
#for loop looks for a match in the data set of IDs with current called ID variable,
#the for loop searches the mapped IDs as a matrix and counts variables r,c while searching
#i.e. looks for the ID on the the r th row and c th column = POSID[r][c], if ID == POSID[r][c]
#the tag position is the current and returns it, if not equal checks for the r th row and c+1 th column
#by this iteration the ID is checed for each element of POSID matrix and returns the distance
#in mm, keep in mind that once an element in POSID is mismatches the ID, increasing the indicators
#ind_c ind_r means cheacking the next tag ID on the physical system.
#
##
#
def find_array(POSID,ID,dist_be_tags):
    try:
        ind_r = 0
        ind_c = 0
        tag = []
        for item_row in POSID:
            for item in item_row:
                if(item.find(ID)) != -1:
                    tag = [ind_c * dist_be_tags, ind_r * dist_be_tags]                             
                ind_c = ind_c + 1
            ind_r = ind_r +1
            ind_c = 0
        return tag
    except:
        print "error in find_array function on fnc_trilateration_node.py"
#
## function: pre_fil_two
#
## INPUT VARIABLES
#dist_be_tags: distance between the passive tags (currently 140mm in the system)
#rssi1: RSSI value of first tag
#rssi2: RSSI value of second tag
#RSSIDIS: data set of matching RSSI values to distance between antenna and tags (table 4.2 M.Sc. thessis of Stephan Vette)
## OUTPUT VARIABLES
#confi1: first possible configuration 
#confi2: second possible configuration
## FUNCTION DESCRIPTION
# function used to convert RSSI values to corresponding distances by validating
# with the condition: distance of tag 1 + distance of tag 2 >= distance between tags
# at max two possible configuration passes validation of geometric constraints
# at worst all configurations fail on validation and returned combi1 = [0,0], combi2 = [0,0]
##
#   
def pre_fil_two(dist_be_tags,rssi1,rssi2,RSSIDIS):
    try:
        # Initialization
        dist1 = []  # Set 1 of all possible distances for rssi1
        dist2 = []  # Set 2 of all possible distances for rssi2
        combi1 = [0, 0]
        combi2 = [0, 0]
        # Split the 2xM list (RSSIDIS) into two 2D lists
        list_rssi = RSSIDIS[0]
        list_dis = RSSIDIS[1]
        # Find the set of distances for both RSSI values
        # Indices for the distances,
        k1 = [index for index, value in enumerate(list_rssi) if value == str(rssi1)] #k1 = possible position of rssi1 on list_rssi
        k2 = [index for index, value in enumerate(list_rssi) if value == str(rssi2)] #k2 = possible position of rssi2 on list_rssi
        # Lists with the distances related to the rssi values
        for i in k1: #add all possible distances of tag 1 to dist1 list
            dist1.append(float(list_dis[i]))
        for i in k2: #add all possible distances of tag 2 to dist2 list
            dist2.append(float(list_dis[i]))
        v = False
        #checks for possible & logical combinations (logic: distance of tag 1 + distance of tag 2 >= distance between tags)
        for n in dist1:
            for m in dist2:
                if n+m >= dist_be_tags and not v:
                    combi1 = [n,m]
                elif n+m >= dist_be_tags and v:
                    combi2 = [n,m]
            v = True
        return combi1, combi2
    except:
        print "error in pre_fil_two function on fnc_trilateration_node.py"

#
## function: pre_fil_three
#   
## INPUT VARIABLES
# dist_be_tags: distance between the passive tags (currently 140mm in the system)
# rssi: RSSI values of the three tags as a list, [data.rssi1,data.rssi2,data.rssi3]
# RSSIDIS: data set of matching RSSI values to distance between antenna and tags (table 4.2 M.Sc. thessis of Stephan Vette)
# tag_all_ex: list of tag IDs in order, [tag1, tag2, tag3, tag1, tag2, tag3]
## OUTPUT VARIABLE
# combi: list of distance valus from tags to the center of antenna combi = [dist1,dist2,dist3]
## FUNCTION DESCRIPTION
# the function finds all possible distances corresponding to respective RSSI value from the table (4.2)
# if a tag has multiple possible distances, this function uses an algorithm(?) to find one logical distance among all possibilities
##
#
def pre_fil_three(dist_be_tags,rssi,RSSIDIS,tag_all_ex):
    try:
        # Inputs
        # Tag_all = [[tag1x, tag1y],[...],[...]]
        # tag1x = tag_all[0][0]
        # Initialization
        dist1 = []  # Set 1 of all possible distances for rssi1
        dist2 = []  # Set 2 of all possible distances for rssi2
        dist3 = []  # Set 3 of all possible distances for rssi3
        combi = [0, 0, 0]

        # Split the 2xM list (RSSIDIS) into two 2D lists
        list_rssi = RSSIDIS[0]
        list_dis = RSSIDIS[1]

        # Find the set of distances for bothh RSSI values
        # Indices for the distances
        k1 = [index for index, value in enumerate(list_rssi) if value == str(rssi[0])] #k1 = possible position of rssi1 on list_rssi
        k2 = [index for index, value in enumerate(list_rssi) if value == str(rssi[1])] #k2 = possible position of rssi2 on list_rssi
        k3 = [index for index, value in enumerate(list_rssi) if value == str(rssi[2])] #k3 = possible position of rssi3 on list_rssi
        # Lists with the distances related to the rssi values
        for i in k1:
            dist1.append(float(list_dis[i])) #add all possible distances of tag 1 to dist1 list
        for i in k2:
            dist2.append(float(list_dis[i])) #add all possible distances of tag 2 to dist2 list
        for i in k3:
            dist3.append(float(list_dis[i])) #add all possible distances of tag 3 to dist3 list
        # Count the number of neighbors
        numNeig = [0,0,0]
        dist_all = [dist1, dist2, dist3]
        for m in range(0,3):
            for n in range(1,3):
                try:
                    if tag_all_ex[m][0] == tag_all_ex[m+n][0]:
                        numNeig[m] = numNeig[m]+1
                    if tag_all_ex[m][1] == tag_all_ex[m+n][1]:
                        numNeig[m] = numNeig[m]+1
                except:
                    pass
        #choose one of the distance out of all possible distances from respective RSSI value, table 4.2
        for k in range(0,len(combi)):
            if numNeig[k] <= 1:
                combi[k] = dist_all[k][0]
            elif numNeig[k] >= 2 and (sum(rssi)-rssi[k])<=2:
                combi[k] = dist_all[k][len(dist_all[k])-1]
        return combi
    except:
        print "error in pre_fil_three function on fnc_trilateration_node.py"
#
## function: pre_fil_four
#
## INPUT VARIABLES
# dist_be_tags: constant value of distance between tags in the physical system (currently 140mm)
# rssi: RSSI values of the three tags as a list, [data.rssi1,data.rssi2,data.rssi3,data.rssi4]
# RSSIDIS: data set of matching RSSI values to distance between antenna and tags (table 4.2 M.Sc. thessis of Stephan Vette)
# tag_all_ex: list of tag IDs in order, [tag1, tag2, tag3, tag4], tagi = [position of tag i in x direction, position of tag i in y direction]
## OUTPUT VARIABLES
# combi:
# tags_final
## FUNCTION DESCRIPTION
# either for 4 or 5 tag reading, pick the 3 tag with highest rssi value and returns 3/5 tag information and the system will
# act from now on as 3 tags are readed
##
#
def pre_fil_four(dist_be_tags,rssi,RSSIDIS,tag_all_ex):
    try:
        tags_final = []
        combi = [0, 0, 0]
        combi_temp = []

        # Split the 2xM list (RSSIDIS) into two 2D lists
        list_rssi = RSSIDIS[0]
        list_dis = RSSIDIS[1]
        #print tag_all_ex
        for k in range(0,len(rssi)):
            ind_temp = list_rssi.index(str(rssi[k])) #ind_temp = each rssi value in the rfid data
            combi_temp.append([float(list_dis[ind_temp]),tag_all_ex[k][0],tag_all_ex[k][1]])
        #combi_temp = [,position of tag i in x direction, position of tag i in y direction]

        # Take the most suitable distances(the ones with the smallest radius)
        # Sorting of the list combi_temp with the smallest distance first (Most accuracy)
        combi_temp = sorted(combi_temp, key=lambda x: x[0])

        for l in range(0,3):
            #print l
            combi[l] = combi_temp[l][0]
            tags_final.append([combi_temp[l][1],combi_temp[l][2]])
        return combi, tags_final
    except Exception as e:
        print "error in pre_fil_four function on fnc_trilateration_node.py"
	print e
#
## function: bilateration_two
#
## INPUT VARIABLES
#combi: calculated combination of tag1 and tag2
#tag1: position of tag 1 in the system, tag1 = [x1,y1]
#tag2: position of tag 2 in the system, tag2 = [x2,y2]
## OUTPUT VARIABLES
# gi_x: gi_x = [xi_+,xi_-] #formula (2.19) in Stephen Vette's M.Sc. Thessis
# gi_y: gi_y = [yi_-,yi_+] #formula (2.20) in Stephen Vette's M.Sc. Thessis
# Note: gi = [gi_x[0],gi_y[0]], gi_complement = [[gi_x[1]],[gi_y[1]]]
# gi and gi_complement are two possible intersection points of circles, refer to figure 2.4 for visualization
## FUNCTION DESCRIPTION
# performs the bilateration explained in 2.2.2 in Stephen Vette's M.Sc. Thessis
##
#    
def bilateration_two(combi,tag1,tag2):
    try:
        d = dist_ptp(tag1,tag2)
        d_jt = (combi[0]**2-combi[1]**2+d**2)/(2*d) #formula (2.17) in Stephen Vette's M.Sc. Thessis
        h = math.sqrt(abs(combi[0]**2-d_jt**2)) #formula (2.14 or 2.15) in Stephen Vette's M.Sc. Thessis
                                                # abs(sqrt(x)) prevent having an error caused by sqrt(-x)

        #formula (2.18), f_t =[x_t,y_t]
        x_t = tag1[0]+(d_jt/d)*(tag2[0]-tag1[0])
        y_t = tag1[1]+(d_jt/d)*(tag2[1]-tag1[1])
        # Temporal solution to get to gix_+ and gix_- , secondary part of the addition on equations (2.19)&(2.20)
        o_x = (h/d)*(tag2[1]-tag1[1])
        o_y = (h/d)*(tag2[0]-tag1[0])
        # intersection point gi = [gi_x,gi_y] formulas (2.19)&(2.20)
        gi_x = [x_t+o_x, x_t-o_x]
        gi_y = [y_t-o_y, y_t+o_y]
        return gi_x, gi_y
    except:
        print "error in bilateration_two function on fnc_trilateration_node.py"

def bilateration_two_no_intersection(combi,tag1,tag2):
    try:
        combi2 = combi
        d = dist_ptp(tag1,tag2)
        # Fix 1st radius
        combi2[0] = d-combi[1]
        d_jt = (combi2[0]**2-combi2[1]**2+d**2)/(2*d)
        x_t_1 = tag1[0]+(d_jt/d)*(tag2[0]-tag1[0])
        y_t_1 = tag1[1]+(d_jt/d)*(tag2[1]-tag1[1])

        # Fix 2nd radius
        combi2[1] = d-combi[0]
        combi2[0] = combi[0]
        d_jt = (combi2[0]**2-combi2[1]**2+d**2)/(2*d)
        x_t_2 = tag1[0]+(d_jt/d)*(tag2[0]-tag1[0])
        y_t_2 = tag1[1]+(d_jt/d)*(tag2[1]-tag1[1])

        gi_x_temp = (x_t_1 + x_t_2)/2
        gi_y_temp = (y_t_1 + y_t_2)/2
        # Temporal solution to get to gix_+ and gix_-
        gi_x = [gi_x_temp, gi_x_temp]
        gi_y = [gi_y_temp, gi_y_temp]

        return gi_x, gi_y
    except:
        print "error in bilateration_two_no_intersection function on fnc_trilateration_node.py"

 #
 ## INPUT VARIABLES
 # combi1: combi list returned from pre_fil_three, combi1 = [rssi1,rssi2,rssi3]
 # tagl_all: tag position list,tag_all = [[x1,y1],[x2,y2],[x3,y3]]
 ## OUTPUT VARIABLE
 # solution: position of the AGV (x,y)
 ## DESCRIPTION
 # performs the trilateration (3xbilateration) for finding the 6 intersection points of 3 circles,
 # then validates and eliminates 1/2 of those points and finally finds the position of the AGV
 ##
 #  
def bilateration_three(combi1,tag_all):
    try:
        g_x_temp = []
        g_y_temp = []
        g_x_all = []   # At the end 3 x lsit of 2 elemets (gi_x_+ and gi_x_-)
        g_y_all = []   # At the end 3 x lsit of 2 elemets (gi_y_+ and gi_y_-)
        g_x_final = []  # The clustered three gi_x, gj_x and gk_x
        g_y_final = []  # The clustered three gi_y, gj_y and gk_y
        solution = [0.0, 0.0]
        boarder_radius = 50 # radius which determines a very accurate estimation of the posiion

        # this loop will find all possible 6 points of intersections between each 2 of 3 circles
        for k in range(0,len(tag_all)):
            # Plausability check no.1 The two circles intersect
            if dist_ptp(tag_all[0],tag_all[1]) <= combi1[0]+combi1[1]:
                g_x_temp,g_y_temp = bilateration_two(combi1[0:2],tag_all[0],tag_all[1])
                # lists have 3 tag information,
                # Rotate the two lists, ex: if a list is [[1,2],[3,4],[5,6]], rotation will result in [[5, 6], [1, 2], [3, 4]]
                # by keeping the algorithm focusing on fixed indexes of the list but shifting the list itself
                # the loop will check the bilateration between tag 1&2,3&1,2&3.
                combi1 = combi1[-1:] + combi1[:-1]
                tag_all = tag_all[-1:] + tag_all[:-1]
                # Store all solutions for g_x and g_y
                g_x_all.append(g_x_temp)
                g_y_all.append(g_y_temp)

            else:
                # Bilateration without intersection
                g_x_temp,g_y_temp = bilateration_two_no_intersection(combi1[0:2],tag_all[0],tag_all[1])
                #Rotate the two lists
                combi1 = combi1[-1:] + combi1[:-1]
                tag_all = tag_all[-1:] + tag_all[:-1]
                # Store all solutions for g_x and g_y
                g_x_all.append(g_x_temp)
                g_y_all.append(g_y_temp)
        # find the three closest intersection points by minimum square euiclidean sum (2.21)&(2.22)
        # Clustering of all values of g_x_+/- to get the correct three ones
        # (n)gn+ = [g_x_all[n][0], g_y_all[n][0]] gi- = [g_x_all[n][1], g_y_all[n][1]]
        # at this point there are 6 possible calculated points from intersection of three circles
        # intersection points are:
        # gi_jk = (g_x_all[0][0],g_y_all[0][0])         (1) (point 1)
        # gi_jk_c = (g_x_all[0][1],g_y_all[0][1])    (2) (point 1 conjugate)
        # gi_jl = (g_x_all[1][0],g_y_all[1][0])         (3) (point 2)
        # gi_jl_c = (g_x_all[1][1],g_y_all[1][1])    (4) (point 2 conjugate)
        # gi_kl = (g_x_all[2][0],g_y_all[2][0])         (5) (point 3)
        # gi_kl_c = (g_x_all[2][1],g_y_all[2][1])    (6) (point 3 conjugate)
        # following for loop calculates all distances between the 6 possible points,
        # save the distance between point i and point j,j' on v1,v2 and
        # save the distance between point i and point k,k' on v3,v4.
        cost = [0, 0] # [psi,phi] (2.21,2.22)
        for k in range(0,len(tag_all)):
            for m in range(0,2):
                v1 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][0], g_y_all[1][0]])
                v2 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][1], g_y_all[1][1]])
                v3 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][0], g_y_all[2][0]])
                v4 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][1], g_y_all[2][1]])

                cost[m] = min([v1,v2]) + min([v3,v4]) # cost[m=0] = psi, cost[m=1]=phi
            # Use cost lsit to decide which value is closer to the other ones
            if cost[0] < cost[1]: # if psi < phi, put gi_+ as corret answer
                g_x_final.append(g_x_all[0][0])
                g_y_final.append(g_y_all[0][0])
            else:# else - psi > phi -, put gi_- as corret answer
                g_x_final.append(g_x_all[0][1])
                g_y_final.append(g_y_all[0][1])
            # rotate the g_x_all listand g_y_all list
            g_x_all = g_x_all[-1:] + g_x_all[:-1]
            g_y_all = g_y_all[-1:] + g_y_all[:-1]
        # Try to optimize the estimation by determining the most accurate radius
        if combi1[0] <= boarder_radius:
            solution[0] = (g_x_final[0]+g_x_final[2])/2
            solution[1] = (g_y_final[0]+g_y_final[2])/2
        elif combi1[1] <= boarder_radius:
            solution[0] = (g_x_final[0]+g_x_final[1])/2
            solution[1] = (g_y_final[0]+g_y_final[1])/2
        elif combi1[2] <= boarder_radius:
            solution[0] = (g_x_final[1]+g_x_final[2])/2
            solution[1] = (g_y_final[1]+g_y_final[2])/2
        else:
            solution[0] = sum(g_x_final)/3
            solution[1] = sum(g_y_final)/3
        return solution
    except:
        print "error in bilateration_three function on fnc_trilateration_node.py"
#
## function: esti_pos
#
## INPUT VARIABLES
#data: new rfid_data
#position_old: previous position of the AGV
#delta: latest delta (sensor) feedback
## OUTPUT VARIABLE
#position_pub: calculated position of the AGV
## FUNCTION DESCRIPTION
#
#
##
#   
def esti_pos(data,position_old,dist_be_tags,delta):
    try:
        # Initialization
        position_pub = position()

        script_dir = os.path.dirname(__file__)
        rel_path1 = "IDPOS_large.txt"
        rel_path2 = "RSSIDISTANCE.txt"
        abs_file_path1 = os.path.join(script_dir, rel_path1)
        abs_file_path2 = os.path.join(script_dir, rel_path2)

        txt_tagid = ''
        txt_rssidis = ''

        # Load TagID - Pos List
        if os.path.isfile(abs_file_path1) == True:
            with open(abs_file_path1) as jason_file:
                POSID = json.load(jason_file)
        else:
            print("No txt-file for TagID to Position")
        # Load RSSI - Dis List
        if os.path.isfile(abs_file_path2) == True:
            with open(abs_file_path2) as jason_file2:
                RSSIDIS = json.load(jason_file2)
        else:
            print("No txt-file for RSSI to Distance")
        #print data.number
        #-------------------------------------------------------------------------
        # Main computation
        if data.number == 1:
           #print("One")
            # Plausability check
            if data.rssi1 == 7:
                # Get the position from ID, Position Tag is also estimated position
                pos_temp = find_array(POSID,data.id1,dist_be_tags)
                position_pub.x_pos = int(pos_temp[0])
                position_pub.y_pos = int(pos_temp[1])
            else:
                # Faulty measurement because the secound tag is missing
                position_pub.x_pos = 0
                position_pub.y_pos = 0

        #-------------------------------------------------------------------------
        elif data.number == 2:
            #print("Two")
            pos_temp = [0,0]
            pos_temp2 = [0,0]
            # Get the position from ID
            tag1 = find_array(POSID,data.id1,dist_be_tags)
            tag2 = find_array(POSID,data.id2,dist_be_tags)
            print(tag1,tag2)
            print(data.id1,data.id2)
            # Plausability check no.1 - two tags next two each other
            if dist_ptp(tag1, tag2) == dist_be_tags:
                # Prefiltering to get the best (max 2) distances
                last_pos = [position_old.x_pos, position_old.y_pos]
                combi1, combi2 = pre_fil_two(dist_be_tags,data.rssi1,data.rssi2,RSSIDIS)
                # Plausability check no.2 - one tag is missing
                if combi1[0] + combi1[1] < (dist_be_tags*1.3) and combi2[0] + combi2[1] < (dist_be_tags*1.3):
                    # Bilateration (max 2)
                    gi_x, gi_y = bilateration_two(combi1,tag1,tag2)
                    # Compute the position by take the midpoint
                    pos_temp[0] = (gi_x[0]+gi_x[1])/2
                    pos_temp[1] = (gi_y[0]+gi_y[1])/2
                    if combi2[0] != 0:  # Another combination of distances possible
                        #print("Another combi possible")
                        gi_x, gi_y = bilateration_two(combi2,tag1,tag2)
                        # Compute the position by take the midpoint
                        pos_temp2[0] = (gi_x[0]+gi_x[1])/2
                        pos_temp2[1] = (gi_y[0]+gi_y[1])/2
                        # Decide for the best esti
                        esti_dist1 = dist_ptp(last_pos,pos_temp)
                        esti_dist2 = dist_ptp(last_pos,pos_temp2)
                        error_esti1 = (esti_dist1-delta)**2
                        error_esti2 = (esti_dist2-delta)**2
                        # Which of both points is more reaistic
                        if error_esti1 <= error_esti2:
                            position_pub.x_pos = int(pos_temp[0])
                            position_pub.y_pos = int(pos_temp[1])
                        else:
                            position_pub.x_pos = int(pos_temp2[0])
                            position_pub.y_pos = int(pos_temp2[1])

                    else:
                        position_pub.x_pos = int(pos_temp[0])
                        position_pub.y_pos = int(pos_temp[1])

                else:
                    position_pub.x_pos = 0
                    position_pub.y_pos = 0

            else:
                # Faulty measurement because the secound tag is missing
                position_pub.x_pos = 0
                position_pub.y_pos = 0

        #-------------------------------------------------------------------------
        elif data.number == 3:
            # Get the position from ID
            tag1 = find_array(POSID,data.id1,dist_be_tags)
            tag2 = find_array(POSID,data.id2,dist_be_tags)
            tag3 = find_array(POSID,data.id3,dist_be_tags)
            tag_all_ex = [tag1, tag2, tag3, tag1, tag2, tag3]
            # Estimate the correct Distances related to RSSI
            rssi = [data.rssi1,data.rssi2,data.rssi3]
            combi1 = pre_fil_three(dist_be_tags,rssi,RSSIDIS,tag_all_ex)

            # Compute the estimated position based on 3 x bilateration
            pos_temp = bilateration_three(combi1,tag_all_ex[0:3])

            position_pub.x_pos = int(pos_temp[0])
            position_pub.y_pos = int(pos_temp[1])
        #-------------------------------------------------------------------------
        # To use an estimation corresponding to 3 tags and 3 radii, the first step is to
        # choose 3 out of 4 or 3 out of 5 detected tags. This is done by the fact that
        # the larger the RSSI values are, the more accurate they are. Based on this, the
        # algorithm is picks the first 3 elements with the highest RSSI values.
        elif data.number == 4 or data.number == 5:
            #print("Four or five")
            # Get the position from ID
            tag1 = find_array(POSID,data.id1,dist_be_tags)
            tag2 = find_array(POSID,data.id2,dist_be_tags)
            tag3 = find_array(POSID,data.id3,dist_be_tags)
            tag4 = find_array(POSID,data.id4,dist_be_tags)
            if data.number == 4: # Estimation with 4 tags
                tag_all_ex = [tag1, tag2, tag3, tag4]
                rssi = [data.rssi1,data.rssi2,data.rssi3,data.rssi4]
            else:               # Estimation with 5 tags or more
                tag5 = find_array(POSID,data.id5,dist_be_tags)
                #tag_all_ex = [tag1, tag2, tag3, tag4, tag5] error tag5 = []
                #rssi = [data.rssi1,data.rssi2,data.rssi3,data.rssi4,data.rssi5]
                tag_all_ex = [tag1, tag2, tag3, tag4]
                rssi = [data.rssi1,data.rssi2,data.rssi3,data.rssi4]

            # Estimate the correct Distances related to RSSI
            #print data.number
            combi1, tags_final = pre_fil_four(dist_be_tags,rssi,RSSIDIS,tag_all_ex)
            # Compute the estimated position based on 3 x bilateration
            pos_temp = bilateration_three(combi1,tags_final)

            position_pub.x_pos = int(pos_temp[0])
            position_pub.y_pos = int(pos_temp[1])
        else:
            #print("no corrcet number of tags")
            position_pub.x_pos = 0
            position_pub.y_pos = 0


        return position_pub
    except:
        print "error in esti_pos function on fnc_trilateration_node.py"
	print data
