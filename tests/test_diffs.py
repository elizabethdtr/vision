import pytest
from skimage.metrics import structural_similarity as ssim
import imutils
import cv2

def func(grayA, grayB):
	(score, diff) = ssim(grayA, grayB, full=True)
	return score


def test_ssim_with_small_difference():
	imageA = cv2.imread("images_diff/ref.bmp")
	imageB = cv2.imread("images_diff/diff_1.bmp")
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

	assert func(grayA, grayB) > 0.7
	assert func(grayA, grayB) < 1
	
def test_ssim_with_big_difference():
	imageA = cv2.imread("images_diff/ref.bmp")
	imageB = cv2.imread("images_diff/11.bmp")
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

	assert func(grayA, grayB) >= 0
	assert func(grayA, grayB) <= 0.7

def test_ssim_without_difference():
	imageA = cv2.imread("images_diff/ref.bmp")
	imageB = cv2.imread("images_diff/ref.bmp")
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

	assert func(grayA, grayB) == 1
