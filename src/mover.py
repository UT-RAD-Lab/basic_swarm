#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Int16MultiArray
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt
import sys

args = rospy.myargv(argv=sys.argv)
rob_number = args[1]
rob_name = 'tb3_' + args[1]
print args

target_x = 0.0
target_y = 0.0
target_yaw = 0.0

x = 0.0
y = 0.0
yaw = 0.0

def poseCallback(msg):
    global target_x
    global target_y
    global target_yaw

    target_x = msg.position.x
    target_y = msg.position.y
    rot = msg.orientation
    (roll, pitch, target_yaw) = euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])

def odomCallback(msg):
    global x
    global y
    global yaw

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    rot = msg.pose.pose.orientation
    (roll, pitch, yaw) = euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])

rospy.init_node('mover_node_' + rob_number, anonymous=True)
rospy.Subscriber('/target', Pose, poseCallback)
rospy.Subscriber('/' + rob_name + '/odom', Odometry, odomCallback)
pub = rospy.Publisher('/targeter', Int16MultiArray, queue_size=10)
pub_speed = rospy.Publisher('/' + rob_name + '/cmd_vel', Twist, queue_size=10)
speed = Twist()

rate = rospy.Rate(10)

while not rospy.is_shutdown():
    delta_x = target_x - x
    delta_y = target_y - y
    delta_yaw = target_yaw - yaw

    angle_to_goal = atan2(delta_y, delta_x)
    distance_to_goal = sqrt((delta_x**2)+(delta_y**2))
    threshold = 0.04


    if distance_to_goal > threshold:
        if abs(angle_to_goal - yaw) < 0.1:
            speed.linear.x = 0.22
            speed.angular.z = 0.0
        elif (angle_to_goal - yaw ) < 0:
            speed.angular.z = -0.3
            speed.linear.x = 0
        elif (angle_to_goal - yaw) > 0:
            speed.angular.z = 0.3
            speed.linear.x = 0
        else:
            speed.angular.z = 0
            speed.linear.x = 0
    elif distance_to_goal <= threshold and abs(delta_yaw) > 0.05:
        if delta_yaw < 0:
            speed.angular.z = -0.3
            speed.linear.x = 0
        elif delta_yaw > 0:
            speed.angular.z = 0.3
            speed.linear.x = 0
        print distance_to_goal
    else:
        speed.angular.z = 0
        speed.linear.x = 0
        rob_array = Int16MultiArray()
        rob_array.data = [int(rob_number), 1]
        pub.publish(rob_array)

    pub_speed.publish(speed)
    rate.sleep()
