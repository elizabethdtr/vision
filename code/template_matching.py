# Extract image differences
#
# Author: Elizabet Dimitrova
# Issued: 31/03/2020

# import necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
import time

start = time.time()
#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="Path to template image")
ap.add_argument("-i", "--images", required=True, help="Path to images where template will be matched")
#ap.add_argument("-v", "--visualize", help="Flag to indicate whether or not to visualize each iteration")
args = vars(ap.parse_args())

#load the image, convert it to grayscale, and detect edges
template = cv2.imread(args["template"])
templateResized = imutils.resize(template, width=677)

#roi_sunglassesCaseBlue = templateResized[45:450, 165:310]
#roi = templateResized[45:450, 165:310]
roi = templateResized

cv2.imshow("ROI", roi)

roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
roi = cv2.Canny(roi, 50, 200)
(tH, tW) = roi.shape[:2]


#loop over the images to find the template in
#for imagePath in glob.glob(args["images"] + "/*.bmp"):
#load the image convert it to grayscale and initialize the bookkeping  variable to keep track of the matched region
image = cv2.imread(args["images"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
found = None
	
#loop over the scales of the image 
for scale in np.linspace(0.2,1.0, 20) [::-1]:
	#resize the image according to the scale and keep track of the ratio of the resizing
	resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
	r = gray.shape[1] / float(resized.shape[1])

	#if the resized image is smaller than the template, then break from the loop
	if resized.shape[0] < tH or resized.shape[1] < tW:
		break
		
	#detect edges in the resized, grayscale image and apply template matching to find the template in the image
	edged = cv2.Canny(resized, 50, 200)
	result = cv2.matchTemplate(edged, roi, cv2.TM_CCOEFF)
	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
	
	#check to see if the iteration should be visualized 
	#if args.get("visualize", False):
		#draw a bounding box around the detected region
		#clone = np.dstack([edged, edged, edged])
		#cv2.rectangle(clone, (maxLoc[0], maxLoc[1]), (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 5)
		#clone = imutils.resize(clone, width=677)
		#cv2.imshow("Visualize", clone)
		#cv2.waitKey(0)
		
	#if we found the maximum correlation value, then update the bookkeeping variable
	if found is None or maxVal > found[0]:
		found = (maxVal, maxLoc, r)
	
#unpack the bookeping variable and compute the (x, y) coordinates of the bunding box based on the resized ratio.
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0]*r), int(maxLoc[1]*r))
(endX, endY) = (int((maxLoc[0]+tW)*r), int((maxLoc[1]+tH)*r))

#draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0,0,255), 5)
image = imutils.resize(image, width=677)
cv2.imshow("Image", image)

end = time.time()
print(end - start)

cv2.waitKey(0)
			
