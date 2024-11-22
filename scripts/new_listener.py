#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def callback(msg):
    rospy.loginfo("I see %s", msg.data)

rospy.init_node('new_listener')
rospy.Subscriber('color_list', String, callback, queue_size=10)
rospy.spin()
