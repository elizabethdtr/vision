# Barcode scanner image application
#
# Author: Elizabet Dimitrova
# Issued: 31/03/2020

#import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
import imutils
import numpy as np

fontSize = 2
rectLineWidth = 10
rectLineColor = (0, 0, 255)

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to imput image")
args = vars(ap.parse_args())

#load the input image
image = cv2.imread(args["image"])

#cap = cv2.VideoCapture(0)
#if not cap.isOpened:
#    print('--(!)Error opening video capture')
#    exit(0)
    
#ret, image = cap.read()
#if image is None:
#        print('--(!) No captured frame -- Break!')
    
image_original = imutils.resize(image, width=677)
cv2.imshow("Original", image_original)
cv2.moveWindow("Original", 0, -3)
cv2.waitKey(2);


#find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)

#loop over the detected barcodes
for barcode in barcodes:
	# extract the boundig box location of the barcode and draw the 
	# bounding box surrounding the barcode on the image
	(x, y, w, h) = barcode.rect
	cv2.rectangle(image, (x, y), (x+w, y+h), rectLineColor, rectLineWidth)
	
	# the barcode data is a bytes object so if we want ot draw it on
	# our output image we need to convert it to a string first
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type
	
	# draw teh barcode data and barcode type on the image
	text = "{} ({})".format(barcodeData, barcodeType)
	cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, fontSize, rectLineColor, rectLineWidth)
	
	# print the barcode type and data to the terminal
	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
	

#cv2.resize(image, (1,1) )
image = imutils.resize(image, width=677 )
cv2.imshow("Barcode detector", image)
cv2.moveWindow("Barcode detector", 700, 0)
cv2.waitKey(0);
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
