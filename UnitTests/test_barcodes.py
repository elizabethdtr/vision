import pytest
import imutils
import cv2
from pyzbar import pyzbar

def func(image):
	barcodes = pyzbar.decode(image)
	return barcodes
	

def test_image_with_barcode():
	image = cv2.imread("images_barcodes/ref.bmp")
	
	assert func(image) != []

def test_image_without_barcode():
	image = cv2.imread("images_barcodes/ref_diff.bmp")
	
	assert func(image) == []
