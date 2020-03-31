# Barcode scanner image application
#
# Author: Elizabet Dimitrova
# Issued: 31/03/2020

from __future__ import print_function
from pyzbar import pyzbar as pyzbar
import numpy as np
import cv2
import imutils
from imutils.video import VideoStream
import time

fontSize = 2
rectLineWidth = 10
rectLineColor = (0, 0, 255)

def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
  print("in decode fucnt", im)
 # print("in decode fucnt", decodedObjects)
  # Print results
  for obj in decodedObjects:

    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
    
  return decodedObjects


# Display barcode and QR code location  
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    #points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    #if len(points) > 4 : 
    #  hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
    #  hull = list(map(tuple, np.squeeze(hull)))
    #else : 
    #  hull = points;
    
    # Number of points in the convex hull
    #n = len(hull)

    # Draw the convext hull
    #for j in range(0,n):
    #  cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
    (x, y, w, h) = decodedObject.rect
    print("[INFO] x y w h", x, y, w, h)
    cv2.rectangle(im, (x, y), (x+w, y+h), rectLineColor, rectLineWidth)
  # Display results 
  #im = imutils.resize(im, width=677 )
  cv2.imshow('Results', im);  
  #cv2.waitKey(0);

  
# Main 
if __name__ == '__main__':

  # Read image
  #im = cv2.imread('gero.jpeg')
  
  print("[INFO] starting video stream... ")
  vs = VideoStream(usePiCamera=True).start()
  time.sleep(2.0)
  
  while True:
    im = vs.read()
    #print("[INFO] read a frame")
    decodedObjects = decode(im)  
    display(im, decodedObjects)
    
    key = cv2.waitKey(1) 
	
    if key == ord("q"):
      break
  
  print("[INFO] cleaning up")
  cv2.destroyAllWindows()
  vs.stop()
