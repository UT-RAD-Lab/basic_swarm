#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import Int16MultiArray

rospy.init_node('planner_node', anonymous=True)

class Turtlebot:
    def __init__(self, publisher, target):
        self.publisher = publisher
        self.target = target

    def setTarget(self):
        if self.target == 1:
            self.target = 2
        elif self.target == 2:
            self.target = 3
        elif self.target == 3:
            self.target = 1

    def publ(self):
        self.publisher.publish()

target1 = Pose()
target1.position.x = -4
target1.position.y = 4
target1.orientation.w = 1

target2 = Pose()
target2.position.x = -4
target2.position.y = 1
target2.orientation.w = 0.707
target2.orientation.z = 0.707

target3 = Pose()
target3.position.x = -1
target3.position.y = 1
target3.orientation.w = 0.707
target3.orientation.z = -0.707

goal_statuses = [1,1,1] #Checks if each robot has reached its target

pub0 = rospy.Publisher('/tb3_0/target', Pose, queue_size=10)
pub1 = rospy.Publisher('/tb3_1/target', Pose, queue_size=10)
pub2 = rospy.Publisher('/tb3_2/target', Pose, queue_size=10)

robots = [Turtlebot(pub0, 1), Turtlebot(pub1, 2), Turtlebot(pub2, 3)]


def intArrayCallback(msg):
    global goal_statuses
    msg_array = msg.data
    goal_statuses[msg_array[0]] = msg_array[1]
    print
    if goal_statuses[0] == 1 and goal_statuses[1] == 1 and goal_statuses == 1:
        goal_statuses = [0,0,0]

        for robot in robots:
            robot.setTarget()
            robot.publ()
        print "did stuff"


sub = rospy.Subscriber('/targeter', Int16MultiArray, intArrayCallback)
first_array = Int16MultiArray()
first_array.data = [0,1]
intArrayCallback(first_array)
rospy.spin()
