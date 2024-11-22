#!/usr/bin/env python3
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
bridge = CvBridge()
  

def CallbackFunction(message):
    bridge=CvBridge()
    rospy.loginfo("received a vdeo")
    converterfromBackToCv=bridge.imgmsg_to_cv2(message,"bgr8") #вооооооооот здесь ошибка

    cv2.rectangle(converterfromBackToCv,(20,20),(200,200),(255,255,0),2)

    cv2.imshow("camera",converterfromBackToCv)
    cv2.waitKey(1)

rospy.init_node("camera_viewer",anonymous=True)

rospy.Subscriber("/usb_cam/image_raw",Image,CallbackFunction)
publisher=rospy.Publisher("/usb_cam/image_raw",Image,queue_size=60)

rate=rospy.Rate(60)
vid_capture = cv2.VideoCapture(0)

while not rospy.is_shutdown():
    returnValue,capturedframe=vid_capture.read()
    if returnValue==True:
        rospy.loginfo("video frame captured and published")
        imageToTransmit=bridge.cv2_to_imgmsg(capturedframe)
        publisher.publish(imageToTransmit)
    rate.sleep()

ate=rospy.Rate(60)

