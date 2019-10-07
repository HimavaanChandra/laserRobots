#!/usr/bin/env python3
#!/usr/bin/env python2

from __future__ import print_function
import rospkg
import pyzbar.pyzbar as pyzbar
import rospy
import numpy as np
import cv2
import time
from vision_ros.msg import vision_comms
import geometry_msgs


xThomasCode = 0
yThomasCode = 0
xLightningCode = 0
yLightningCode = 0


def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    for obj in decodedObjects: #maybe adjust this for printing
        print('')     
    return decodedObjects

pub = rospy.Publisher('robot_positions', vision_comms, queue_size=10)
rospy.init_node('robot_positions', anonymous=True)
rate = rospy.Rate(10)  #10hz



cap = cv2.VideoCapture(0)

cap.set(3,1920)
cap.set(4,1080)
time.sleep(2)

font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        #print(x, y)
        qrData = decodedObject.data

        if qrData == b'1':
              xThomasCode = x
              yThomasCode = y
              print("Thomas: ",xThomasCode,yThomasCode)
              cv2.putText(frame, 'Thomas', (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
        if qrData == b'2':
              xLightningCode = x
              yLightningCode = y
              print("Lightning: ",xLightningCode,yLightningCode)
              cv2.putText(frame, 'Lightning', (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)


        barCode = str(decodedObject.data)
        # cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
    
    if not rospy.is_shutdown():
      msg = vision_comms()
      msg.xThomas = xThomasCode
      msg.yThomas = yThomasCode
      msg.xLightning = xLightningCode
      msg.yLightning = yLightningCode
      rospy.loginfo(msg)
      pub.publish(msg)
      rate.sleep()             

    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
   

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()