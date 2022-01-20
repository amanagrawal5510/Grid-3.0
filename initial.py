import cv2
import numpy as np

  
def cordi(img):
    cv2.imshow('image', img)
    ret=()

    #define the events for the
    # mouse_click.
    def mouse_click(event, x, y, 
                    flags, param):

        # to check if left mouse 
        # button was clicked
        if event == cv2.EVENT_LBUTTONDOWN:

            # font for left click event
            font = cv2.FONT_HERSHEY_TRIPLEX
            LB = f'{x} {y}'
            ret= (x, y)

            # display that left button 
            # was clicked.
            cv2.putText(img, LB, (x, y), 
                        font, 1, 
                        (255, 255, 0), 
                        2) 
            cv2.imshow('image', img)


        # to check if right mouse 
        # button was clicked
        if event == cv2.EVENT_RBUTTONDOWN:

            # font for right click event
            font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
            RB = 'Right Button'

            # display that right button 
            # was clicked.
            cv2.putText(img, RB, (x, y),
                        font, 1, 
                        (0, 255, 255),
                        2)
            cv2.imshow('image', img)

    cv2.setMouseCallback('image', mouse_click)

    cv2.waitKey(0)

    # close all the opened windows.
    cv2.destroyAllWindows()
    return ret
  
# cv2.setMouseCallback('image', mouse_click)

def first(img):
    dictitionary={}
    for i in range(1, 13):
        dictitionary[i]= cordi(img)

    for i in range(97, 101):
        dictitionary[i]= cordi(img)
    
    return dictitionary




