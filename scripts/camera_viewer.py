#!/usr/bin/env python3
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
bridge = CvBridge()


def image_callback(img):
    i=0
    while i< 1000:

        cv_image = bridge.imgmsg_to_cv2(img,"bgr8")
        
        cv2.rectangle(cv_image,(20,20),(200,200),(255,255,0),2)
        cv2.imshow('Video frame',cv_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
         break
        i+=1
   


    

rospy.init_node('camera_viewer')
rospy.Subscriber('/usb_cam/image_raw', Image , image_callback, queue_size=10)
# pub = rospy.Publisher('/contour_color', ( gthtvtyyfz dsdjlf), queue_size=10)
# rospy.spin()