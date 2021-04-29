#!/usr/bin/env python
import rospy, os, json, math
from std_msgs.msg import String
from pipeless_plant_master.msg import rfid_data
from pipeless_plant_master.msg import position

def dist_ptp(p1,p2):
    dist = math.sqrt((p2[1]-p1[1])**2+(p2[0]-p1[0])**2)
    return dist 

def find_array(POSID,ID,dist_be_tags):
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
    # if not tag:
    #     tag = [0,0]
    return tag
#
def main ():
    script_dir = os.path.dirname(__file__)
    rel_path1 = "IDPOS.txt"
    rel_path2 = "RSSIDISTANCE.txt"
    rel_path3 = "Meas_desktop10.txt"
    abs_file_path1 = os.path.join(script_dir, rel_path1)
    abs_file_path2 = os.path.join(script_dir, rel_path2)
    abs_file_path3 = os.path.join(script_dir, rel_path3)
    
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
    file = open(abs_file_path3, 'r')
    txt_data = file.readlines(2)   # txt_data contains the whole textfile
    file.close()

    # check if each ID in the ID data set are in the tag field data set
    # gl_count = 0
    # while gl_count < len(txt_data):
    #     step = int(txt_data[gl_count])
    #     for x in range(gl_count,gl_count+step): # loop from the current till the end of tags of each data series ( x = from gl_count = 0 to gl_count+step = 0+4) 
    #         temp = txt_data[x+1].split() # save the current+1 into temp as a list with two elements temp[0]= tag id, temp[1] = RSSI value of that tag, (x=0 temp ='DCEB','0'],x=1 temp= ['DCEB', '0'],x=2 temp=['E757','0'],x=3 temp=['D992','0']) 
    #         #print(temp[0]) # save the that id to id_list, (x=0 id_list[0]=id_list[0-0]=temp[0]=DCEB, x=1 id_list[1]=id_list[1-0]=temp[0]=D75A, and so on)
    #         found = False
    #         for i in range(0,len(POSID)):
    #             for j in range(0,len(POSID[1])):
    #                 if(temp[0] == POSID[i][j]):
    #                     found = True
    #                     break
    #             if found:
    #                 break
    #         if not found:
    #             print temp[0]
    #     gl_count = gl_count + step + 1 

    # dist_be_tags = 140
    # id1 = 'D75A'
    # id2 = 'D992'
    # id3 = 'D98A'
    # tag1 = find_array(POSID,id1,dist_be_tags)
    # tag2 = find_array(POSID,id2,dist_be_tags)
    # tag3 = find_array(POSID,id3,dist_be_tags)
    # tag_all_ex = [tag1, tag2, tag3, tag1, tag2, tag3]
    # print tag_all_ex
    
    tag_all = [[420.0,140.0],[560,140],[140,420]]
    # tag_all  =[[1,2],[3,4],[5,6]]
    # combi1 = [120.0,120.0,90.0]            
    # combi1_edited = combi1[-1:] + combi1[:-1]
    # tag_all_edited = tag_all[-1:] + tag_all[:-1]
    # print "     tag:{}      combi:{}".format(tag_all,combi1)
    # print "tag edit:{} combi edit:{}".format(tag_all_edited,combi1_edited)
    # print combi1[-1:]
    # print combi1[:-1]
    # print tag_all[-1:]
    # print tag_all[:-1]
    g_x_temp = []
    g_y_temp = []
    g_x_all = []   # At the end 3 x lsit of 2 elemets (gi_x_+ and gi_x_-)
    g_y_all = []   # At the end 3 x lsit of 2 elemets (gi_y_+ and gi_y_-)
    g_x_final = []  # The clustered three gi_x, gj_x and gk_x
    g_y_final = []  # The clustered three gi_y, gj_y and gk_y
    g_x_all = [[490.0, 490.00], [335.14, 335.14], [214.88, 214.88]]
    g_y_all = [[42.53, 237.46], [224.85, 224.85], [370.07, 370.07]]

    g_x_all = [[1,2],[3,4],[5,6]]
    g_y_all = [[7,8],[9,10],[11,12]]
    # print '++'
    cost = [0, 0]
    print POSID
    # for k in range(0,len(tag_all)):
    #     print "gxa:{}".format(g_x_all)
    #     print "gya:{}".format(g_y_all)
    #     print "k:{}".format(k)
    #     for m in range(0,2):
    #         print "m:{}".format(m)
    #         v1 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][0], g_y_all[1][0]])
    #         v2 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][1], g_y_all[1][1]])
    #         v3 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][0], g_y_all[2][0]])
    #         v4 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][1], g_y_all[2][1]])
            
    #         print"v1:{},{},{}".format([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][0], g_y_all[1][0]],v1)
    #         print"v2:{},{},{}".format([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][1], g_y_all[1][1]],v2)
    #         print"v3:{},{},{}".format([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][0], g_y_all[2][0]],v3)
    #         print"v4:{},{},{}".format([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][1], g_y_all[2][1]],v4)
    #         print "min1: {},min2:{}".format(min([v1,v2]) , min([v3,v4]))
    #         cost[m] = min([v1,v2]) + min([v3,v4])
    #         print"cost:{}".format(cost)
    #     # Use cost lsit to decide which value is closer to the other ones
    #     if cost[0] < cost[1]:
    #         # put gi_+ as corret answer
    #         g_x_final.append(g_x_all[0][0])
    #         g_y_final.append(g_y_all[0][0])
    #     else:
    #         # put gi_- as corret answer
    #         g_x_final.append(g_x_all[0][1])
    #         g_y_final.append(g_y_all[0][1])
    #     # rotate the g_x_all listand g_y_all list  
    #     g_x_all = g_x_all[-1:] + g_x_all[:-1]
    #     g_y_all = g_y_all[-1:] + g_y_all[:-1]
    #     g_x_all = g_x_all[-1:] + g_x_all[:-1]
    #     g_y_all = g_y_all[-1:] + g_y_all[:-1] 
    #     print"gxf:{}".format(g_x_final) 
    #     print"gyf:{}".format(g_x_final) 
    #     print '####'
    
    # print g_y_all[0][1]
    # print dist_ptp([g_x_all[0][1], g_y_all[0][1]],[g_x_all[1][0], g_y_all[1][0]])
    
    # for k in range(0,len(tag_all)):
    #     for m in range(0,2):
    #         v1 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][0], g_y_all[1][0]])
    #         v2 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[1][1], g_y_all[1][1]])
    #         v3 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][0], g_y_all[2][0]])
    #         v4 = dist_ptp([g_x_all[0][m], g_y_all[0][m]],[g_x_all[2][1], g_y_all[2][1]])
            
    #         cost[m] = min([v1,v2]) + min([v3,v4])
    #     # Use cost lsit to decide which value is closer to the other ones
    #     if cost[0] < cost[1]:
    #         # put gi_+ as corret answer
    #         g_x_final.append(g_x_all[0][0])
    #         g_y_final.append(g_y_all[0][0])
    #     else:
    #         # put gi_- as corret answer
    #         g_x_final.append(g_x_all[0][1])
    #         g_y_final.append(g_y_all[0][1])
    #     # rotate the g_x_all listand g_y_all list  
    #     g_x_all = g_x_all[-1:] + g_x_all[:-1]
    #     g_y_all = g_y_all[-1:] + g_y_all[:-1]   


if __name__ == '__main__':  
    main()
