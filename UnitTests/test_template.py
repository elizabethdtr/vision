# import necessary packages
import numpy as np
import pytest
import cv2
import imutils

def func(gray, roi, tH, tW):
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

		#if we found the maximum correlation value, then update the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
	
	
	#result = cv2.matchTemplate(edged, roi, cv2.TM_CCOEFF)
	
	return maxVal

def test_with_right_template():
	image = cv2.imread("images_template/acquired.bmp")
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
	template = cv2.imread("images_template/t.bmp")
	roi = template[950:1500, 980:1450]
	roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	roi = cv2.Canny(roi, 50, 200)
	(tH, tW) = roi.shape[:2]
	
	assert func(gray, roi, tH, tW) < 0
	
def test_with_wrong_template():
	image = cv2.imread("images_template/acquired.bmp")
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	roi = cv2.imread("images_template/11.bmp")
	roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	roi = cv2.Canny(roi, 50, 200)
	(tH, tW) = roi.shape[:2]
	
	
	assert func(gray, roi, tH, tW) > 0
	assert func(gray, roi, tH, tW) <= 1000000
	
def test_with_same_image():
	image = cv2.imread("images_template/acquired.bmp")
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	roi = cv2.imread("images_template/acquired.bmp")
	roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	roi = cv2.Canny(roi, 50, 200)
	(tH, tW) = roi.shape[:2]
	
	assert func(gray, roi, tH, tW) > 10000000
