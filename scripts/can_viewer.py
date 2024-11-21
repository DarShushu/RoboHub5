#!/usr/bin/env python3
import rospy
from cv_bridge import CvBridge
import cv2
from sensor_msgs.msg import Image

#publisherNodeName="camera_sensor_publisher"
#topicName="video_topic"

def CallbackFunction(message):
    bridge=CvBridge()
    rospy.loginfo("received a vdeo")
    converterfromBackToCv=bridge.imgmsg_to_cv2(message) #вооооооооот здесь ошибка

    cv2.imshow("camera",converterfromBackToCv)
    cv2.waitKey(1)

rospy.init_node("camera_viewer",anonymous=True)

rospy.Subscriber("/usb_cam/image_raw",Image,CallbackFunction)
publisher=rospy.Publisher("/usb_cam/image_raw",Image,queue_size=60)

rate=rospy.Rate(60)
vid_capture = cv2.VideoCapture(0)
bridge = CvBridge()




while not rospy.is_shutdown():
    returnValue,capturedframe=vid_capture.read()
    if returnValue==True:
        rospy.loginfo("video frame captured and published")
        imageToTransmit=bridge.cv2_to_imgmsg(capturedframe)
        publisher.publish(imageToTransmit)
    rate.sleep()



def img_callback(img):
    #rospy.loginfo("I heard %s", img.data)
    while True:

        cv_image = bridge.imgmsg_to_cv2(img, 'brg8')
        cv2.imshow("frame",cv_image)
        vid_capture = cv2.VideoCapture(cv_image)
        _,frame=vid_capture.read()
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    bridge.release()
    cv2.destroyallWindows()




pub = rospy.Subscriber('/usb_cam/image_raw', Image, img_callback, queue_size=10)
rospy.spin()


