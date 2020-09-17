#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty


def main():
    rospy.init_node("init_localize")
    rospy.wait_for_service("global_localization")
    try:
        localize = rospy.ServiceProxy("global_localization", Empty)
        req = localize()
    except rospy.ServiceException as e:
        rospy.log_warn("Service call failed: %s" % e)


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
