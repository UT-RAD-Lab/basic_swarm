#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty


def main():
    rospy.init_node("init_localize")
    rospy.sleep(2)
    rospy.wait_for_service("global_localization")
    try:
        localize = rospy.ServiceProxy("global_localization", Empty)
        req = localize()
        rospy.loginfo("Calling global_localization service")
    except rospy.ServiceException as e:
        rospy.logwarn("Service call failed: %s" % e)


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
