# Extract image differences
#
# Author: Elizabet Dimitrova
# Issued: 31/03/2020

# import necessary packages
from skimage.metrics import structural_similarity as ssim
import argparse
import imutils
import cv2

# construct the argument parse and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True, help="first input image")
ap.add_argument("-s", "--second", required=True, help="second input image")
args = vars(ap.parse_args())

# load the two input images
imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the SSIM between the two images
(score, diff) = ssim(grayA, grayB, full=True)
diff = (diff*255).astype("uint8")
print("SSIM: {}".format(score))

# threshold the difference image, find the countours
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.PETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
	(x, y, w, h) = cv2.boundingRect(c)
	cv2.rectangle(imageA, (x, y), (x+w, y+h), (0,0,255), 2)
	cv2.rectangle(imageB, (x, y), (x+w, y+h), (0,0,255), 2)
	
# show the output images
imageA = imutils.resize(imageA, width=677)
imageB = imutils.resize(imageB, width=677)
diff = imutils.resize(diff, width=677)
thresh = imutils.resize(tresh, width=677)
cv2.imshow("Originial", imageA)
cv2.imshow("Modified", imageB)
cv2.imshow("Diff", diff)
cv2.imshow("Thresh", thresh)

#cv2.destroyAllWindows()
cv2.waitKey(0)
	
	
	
