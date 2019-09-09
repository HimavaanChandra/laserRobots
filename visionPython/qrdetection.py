import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
#import sys
#import time


cap = cv2.VideoCapture(0)
hasFrame = cap.read() #hasFrame,frame = cap.read()

# Display barcode and QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points
    #print(points)   #points needs to be ROS published
    # print(np.array(1))
    # Number of points in the convex hull

    if zbarData == b'1':   #maybe b'1'
          print("Thomas")
          print(points)
    if zbarData == b'2':
          print("Lightning")
          print(points)

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
    if zbarData:
        cv2.putText(inputImage, "ZBAR : {}".format(zbarData), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(inputImage, "ZBAR : QR Code NOT Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    display(inputImage, decodedObjects)
    cv2.imshow("Result",inputImage)

    k = cv2.waitKey(20)
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()