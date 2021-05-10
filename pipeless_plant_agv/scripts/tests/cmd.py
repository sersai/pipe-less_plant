#!/usr/bin/env python
import struct
import unicodedata
import rospy
#this will allow to input values such as -200mm which will be converted automatically
# x = -200
# hi,lo = struct.pack('>h', x)
# print("high: {} low: {}".format(hi,lo)) # what we want but hi & lo are type 'str'

# hi = int(hi.encode('hex'),16)
# lo = int(lo.encode('hex'),16)
# print("high: {} low: {}".format(hi,lo))
# print("high: {} low: {}".format(chr(hi),chr(lo))) # what we want correctly
def main():
    # rospy.init_node('prefilter_enc',disable_signals=True)
    rospy.init_node('prefilter_enc')
    rate = rospy.Rate(4)
    while not rospy.is_shutdown():
        # x = 0/0
        print "loop"
        rate.sleep()
if __name__ == '__main__':
    # main()
    # print "main"
    try:
        main()
        print "main"
    except KeyboardInterrupt:
        print("\n Disconnected")


# def main():
#     rospy.init_node('prefilter_enc')
#     rate = rospy.Rate(4)
#     while not rospy.is_shutdown():
#         x = 0/0
#         print "loop"
#         rate.sleep()
# if __name__ == '__main__':
#     # main()
#     # print "main"
#     try:
#         main()
#         print "main"
#     except:
#         print("Disconnected")
