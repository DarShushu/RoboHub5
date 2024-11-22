#!/usr/bin/env python3
import rospy

import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
bridge = CvBridge()
from std_msgs.msg import String



def CallbackFunction(message):
    bridge=CvBridge()
    msg = String()
    color = []
    rospy.loginfo("received a vdeo")
    img=bridge.imgmsg_to_cv2(message,"bgr8") #вооооооооот здесь ошибка
    # начало цикла обработки

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # HSV
    img_red = cv2.inRange(hsv, (0, 50, 50), (13, 255, 255)) #цвета в hsv
    img_red += cv2.inRange(hsv, (170, 50, 50), (180, 255, 255)) #цвета в hsv
    contours_red, _  = cv2.findContours(img_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours_red:
        if cv2.contourArea(cont) > 3000:
            x, y, w, h = cv2.boundingRect(cont)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

            cv2.putText(img, "red", (x+w//2-20, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            flag = False
            for col in color:
                if col == "red":
                    flag = True
            if flag == False:
                color.append("red")

    img_orange = cv2.inRange(hsv, (15, 50, 50), (20, 255, 255)) #цвета в hsv
    contours_orange, _  = cv2.findContours(img_orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours_orange:
        if cv2.contourArea(cont) > 3000:
            x, y, w, h = cv2.boundingRect(cont)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 69, 255), 2)

            cv2.putText(img, "orange", (x+w//2-20, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            flag = False
            for col in color:
                if col == "orange":
                    flag = True
            if flag == False:
                color.append("orange")

    img_yellow = cv2.inRange(hsv, (25, 50, 50), (33, 255, 255)) #цвета в hsv
    contours_yellow, _  = cv2.findContours(img_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours_yellow:
        if cv2.contourArea(cont) > 3000:
            x, y, w, h = cv2.boundingRect(cont)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)

            cv2.putText(img, "yellow", (x+w//2-20, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            flag = False
            for col in color:
                if col == "yellow":
                    flag = True
            if flag == False:
                color.append("yellow")

    img_green = cv2.inRange(hsv, (35, 50, 50), (75, 255, 255)) #цвета в hsv
    contours_green, _  = cv2.findContours(img_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours_green:
        if cv2.contourArea(cont) > 3000:
            x, y, w, h = cv2.boundingRect(cont)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.putText(img, "green", (x+w//2-20, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            flag = False
            for col in color:
                if col == "green":
                    flag = True
            if flag == False:
                color.append("green")

    img_blue = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255)) #цвета в hsv
    contours_blue, _  = cv2.findContours(img_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours_blue:
        if cv2.contourArea(cont) > 3000:
            x, y, w, h = cv2.boundingRect(cont)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.putText(img, "blue", (x+w//2-20, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            flag = False
            for col in color:
                if col == "blue":
                    flag = True
            if flag == False:
                color.append("blue")
    print(color)
    # create string colors
    msg= ' '.join(color)
    pub.publish(msg)
    
    #обнуление
    msg=""

    for col in color:
        color.pop

     #конец обработки

    cv2.imshow("wow it works too!!",img)
    cv2.waitKey(1)

rospy.init_node("camera_viewer",anonymous=True)

rospy.Subscriber("/usb_cam/image_raw",Image,CallbackFunction)
publisher=rospy.Publisher("/usb_cam/image_raw",Image,queue_size=60)
pub = rospy.Publisher('color_list', String, queue_size=10)



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

