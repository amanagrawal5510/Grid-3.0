'''
AUTHOR: Ayush Tripathi
creates a bounding box around the bodies
no need of imutils, functions can be written in cv2
'''

from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

#define the lower and upper boundaries of the "blue"
blueLower = (104, 186, 0)
blueUpper = (134, 255, 255)
#define the lower and upper boundaries of the "green"
greenLower = (42, 234, 0)
greenUpper = (88, 255, 255)
#define the lower and upper boundaries of the "yellow"
yellowLower = (21, 212, 6)
yellowUpper = (43, 255, 255)
#define the lower and upper boundaries of the "red"
redLower = (0, 224, 0)
redUpper = (14, 255, 255)

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
cap = cv2.VideoCapture('Arena_Prototype.mp4')

frame_width = 600
frame_height = 321

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10.0, (frame_width,frame_height))
# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Display the resulting frame
    frame = imutils.resize(frame, width=600)
    print(frame.shape)
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct masks for the different colors, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)

    mask_green = cv2.inRange(hsv, greenLower, greenUpper)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)

    mask_yellow = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
    mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)

    mask_red = cv2.inRange(hsv, redLower, redUpper)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.dilate(mask_red, None, iterations=2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # draw a rectangle on around it
        c_b = max(cnts, key=cv2.contourArea)
        (x,y,w,h) = cv2.boundingRect(c_b)
        if w > 10 and h > 10:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY = str(x+w/2) + ', '+ str(y+h/2)
            cv2.putText(frame, strXY, (15, 25), font, .5, (255, 0, 0), 2)

    # find contours in the mask and initialize the current
    cnts = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # draw a rectangle on around it
        c_g = max(cnts, key=cv2.contourArea)
        (x,y,w,h) = cv2.boundingRect(c_g)
        if w > 10 and h > 10:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY = str(x+w/2) + ', '+ str(y+h/2)
            cv2.putText(frame, strXY, (15, 75), font, .5, (0, 255, 0), 2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # draw a rectangle on around it
        c_y = max(cnts, key=cv2.contourArea)
        (x,y,w,h) = cv2.boundingRect(c_y)
        if w > 10 and h > 10:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY = str(x+w/2) + ', '+ str(y+h/2)
            cv2.putText(frame, strXY, (15,125), font, .5, (0, 255, 255), 2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # draw a rectangle on around it
        c_r = max(cnts, key=cv2.contourArea)
        (x,y,w,h) = cv2.boundingRect(c_r)
        if w > 10 and h > 10:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY = str(x+w/2) + ', '+ str(y+h/2)
            cv2.putText(frame, strXY, (15, 175), font, .5, (0, 0,255), 2)
    out.write(frame)
    cv2.imshow('Frame',frame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  # Break the loop
  else:
    break
# When everything done, release the video capture object
cap.release()
out.release()
# Closes all the frames
cv2.destroyAllWindows()
