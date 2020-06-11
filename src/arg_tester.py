#! /usr/bin/env python

import sys
import rospy

rospy.init_node('arg_node', anonymous=True)

args = rospy.myargv(argv=sys.argv)
print args
for x in args:
    print x
