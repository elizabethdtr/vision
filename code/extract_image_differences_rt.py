# Extract image differences
#
# Author: Elizabet Dimitrova
# Issued: 31/03/2020

# import necessary packages
from skimage.metrics import structural_similarity as ssim
import argparse
import imutils
import cv2
import time
from imutils.video import VideoStream

start = time.time()

# construct the argument parse and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True, help="first input image")
args = vars(ap.parse_args())

# load the two input images
imageA = cv2.imread(args["first"])

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayA = imutils.resize(grayA, width=600, height=600)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=600, height=600)

	grayB = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	# compute the SSIM between the two images
	(score, diff) = ssim(grayA, grayB, full=True)
	diff = (diff*255).astype("uint8")
	print("SSIM: {}".format(score))
	
	# threshold the difference image, find the countours
	thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	
	# loop over the contours
	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		#cv2.rectangle(imageA, (x, y), (x+w, y+h), (0,0,255), 2)
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
		
		# show the output images
	imageA = imutils.resize(imageA, width=600)
	#imageB = imutils.resize(frame, width=677)
	diff = imutils.resize(diff, width=677)
	thresh = imutils.resize(thresh, width=677)
	cv2.imshow("Originial", imageA)
	cv2.imshow("Modified", frame)
	cv2.imshow("Diff", diff)
	cv2.imshow("Thresh", thresh)
	
	key = cv2.waitKey(1) & 0xFF
	
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
		
cv2.destroyAllWindows()

end = time.time()
print(end-start)
vs.stop()
	
	
	
