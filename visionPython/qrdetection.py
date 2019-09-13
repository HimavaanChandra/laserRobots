import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import roslibpy as ros
#import sys
#import time


cap = cv2.VideoCapture(0)
hasFrame = cap.read() #hasFrame,frame = cap.read()

# Display barcode and QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    if zbarData == b'1':   #points needs to be ROS published  , also store position in a variable and calculate angle using pythagoras maybe
          print("Thomas")
          print(points)
    if zbarData == b'2':
          print("Lightning") #points needs to be ROS published  , also store position in a variable and calculate angle using pythagoras maybe
          print(points)
    # If the points do not form a quad, find convex hull

    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points
    #print(points)   

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

  # Display results
      cv2.imshow("Results", im) #can remove

# Detect and decode the qrcode
#t = time.time()
while(1):   #here put the 2 different qr options
    hasFrame, inputImage = cap.read()
    if not hasFrame:
        break
    decodedObjects = pyzbar.decode(inputImage)
    if len(decodedObjects):
        zbarData = decodedObjects[0].data
    else:
        zbarData=''     

    if zbarData == b'1':
        cv2.putText(inputImage, "Thomas: Found", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(inputImage, "Thomas: Not Found", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    if zbarData == b'2':
        cv2.putText(inputImage, "Lightning: Found", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(inputImage, "Lightning: Not Found", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    display(inputImage, decodedObjects)
    cv2.imshow("Result",inputImage)

    k = cv2.waitKey(20)
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()