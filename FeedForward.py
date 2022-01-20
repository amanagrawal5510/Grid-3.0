'''
AUTHOR: Surya Prakash Mishra
Still uses HSV tracker, working with template
Line and color shifts if body of interest is 10 units far
Give a pause at end point to throw and while changing body of interest 
Can work at an avg FPS of 21, max 25 in 8 GB RAM
Still havent used multiprocessing
'''


import numpy as np
import cv2
import time
import warnings
warnings.filterwarnings('ignore')

CONTOURX, CONTOURY= 0, 0
fail=0


def nothing(x):
    pass
def destroy():
    cv2.destroyAllWindows()


colors= ['blue', 'green', 'red', 'yellow']

# for masking
l_b= np.array([[104, 186, 0], [42, 234, 0], [0, 224, 0], [21, 212, 6]])
h_b= np.array([[134, 255, 255], [88, 255, 255], [14, 255, 255], [43, 255, 255]])

# since camera is static landamrks can be fixed
# landmarks 
pos_1 = np.array([[571.05, 34.05], [643.05, 34.0], [715.05, 34.05], [787.05, 34.05]])   # strarting position
pos_2 = np.array([[571.05, 610], [643.05, 682], [715.05, 683], [787.05, 609.05]])       # L corner
pos_3 = np.array([[48.0, 610], [48.0, 682], [1316, 683], [1316, 609.05]])               # final position

# find center
def center(image):
    global CONTOURX, CONTOURY
    global fail
    try:
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    except:
        gray=image
    edged = cv2.Canny(gray, 50, 200)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        # Sort by left to right using our x_cord_contour function
        contours_left_to_right = sorted(contours, key = cv2.contourArea, reverse = True)
        M = cv2.moments(contours_left_to_right[0])
        cx = round((M['m10'] / (M['m00']+ 1e-8)), 2)
        cy = round((M['m01'] / (M['m00']+ 1e-8)), 2)
        CONTOURX, CONTOURY = cx, cy
        return cx, cy
    except:
        fail+=1
        return CONTOURX, CONTOURY 

# play around to create more robut mask
def actual_pos(color, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.erode(hsv, None, iterations=2)
    hsv = cv2.dilate(hsv, None, iterations=2)
    mask = cv2.inRange(hsv, l_b[color], h_b[color])
    mask = cv2.medianBlur(mask,5)
    cx, cy = center(mask)
    show = cv2.circle(frame.copy(), (int(cx), int(cy)), 3, (0, 0, 0), -1)
    return cx, cy, show, hsv



def ref_line(color, motion, frame, cx, cy):
    dis =0
    error = 0
    if(motion=='D'):
        show = cv2.line(frame.copy(), (0, int(pos_2[color][1])), (frame.shape[1], int(pos_2[color][1])), (250, 0, 200), 1, cv2.LINE_AA)
        show = cv2.line(show, (int(pos_2[color][0]), 0), (int(pos_2[color][0]), frame.shape[0]), (250, 0, 200), 1, cv2.LINE_AA)
        dis = abs(pos_2[color][1]- cy)
        error= abs(pos_2[color][0]- cx)
    if(motion=='U'):
        show = cv2.line(frame.copy(), (0, int(pos_1[color][1])), (frame.shape[1], int(pos_1[color][1])), (250, 0, 200), 1, cv2.LINE_AA)
        show = cv2.line(show, (int(pos_1[color][0]), 0), (int(pos_1[color][0]), frame.shape[0]), (250, 0, 200), 1, cv2.LINE_AA)
        dis = abs(pos_1[color][1]- cy)
        error= abs(pos_1[color][0]- cx)
    if(motion=='L'):
        if(color<2):    # blue, green first go left and then right
            show = cv2.line(frame.copy(), (0, int(pos_3[color][1])), (frame.shape[1], int(pos_3[color][1])), (250, 0, 200), 1, cv2.LINE_AA)
            show = cv2.line(show, (int(pos_3[color][0]), 0), (int(pos_3[color][0]), frame.shape[0]), (250, 0, 200), 1, cv2.LINE_AA)
            dis = abs(pos_3[color][0]- cx)
            error= abs(pos_3[color][1]- cy)
        else:           # red, yellow first opposite to blue green
            show = cv2.line(frame.copy(), (0, int(pos_2[color][1])), (frame.shape[1], int(pos_2[color][1])), (250, 0, 200), 1, cv2.LINE_AA)
            show = cv2.line(show, (int(pos_2[color][0]), 0), (int(pos_2[color][0]), frame.shape[0]), (250, 0, 200), 1, cv2.LINE_AA)
            dis = abs(pos_2[color][0]- cx)
            error= abs(pos_2[color][1]- cy)
    if(motion=='R'):
        if(color<2):
            show = cv2.line(frame.copy(), (0, int(pos_2[color][1])), (frame.shape[1], int(pos_2[color][1])), (250, 0, 200), 1, cv2.LINE_AA)
            show = cv2.line(show, (int(pos_2[color][0]), 0), (int(pos_2[color][0]), frame.shape[0]), (250, 0, 200), 1, cv2.LINE_AA)
            dis = abs(pos_2[color][0]- cx)
            error= abs(pos_2[color][1]- cy)
        else:
            show = cv2.line(frame.copy(), (0, int(pos_3[color][1])), (frame.shape[1], int(pos_3[color][1])), (250, 0, 200), 1, cv2.LINE_AA)
            show = cv2.line(show, (int(pos_3[color][0]), 0), (int(pos_3[color][0]), frame.shape[0]), (250, 0, 200), 1, cv2.LINE_AA)
            dis = abs(pos_3[color][0]- cx)
            error= abs(pos_3[color][1]- cy)
    
    return show, dis, error



def control(color, motion, dis):
    if dis > 10:
        return color, motion
    else:
        if(motion=="U"):
            # print(f'color change from {colors[color]} to next')
            if(color!=3):
                color+=1
                motion="D"
            return color, motion
        else:
            if(color<2):
                # print(f'{colors[color]}  entered with {dis} while going {motion}')
                if(motion=='R'):
                    motion='U'
                elif(motion=='L'):
                    motion='R'
                elif(motion=='D'):
                    motion='L'
                return color, motion
            else:
                # print(f'{colors[color]}  entered with {dis} while going {motion}')
                if(motion=='L'):
                    motion='U'
                elif(motion=='R'):
                    motion='L'
                elif(motion=='D'):
                    motion='R'
                return color, motion
        


cap = cv2.VideoCapture('Sample Video.mp4')
frame_width, frame_height = 728, 1360
out = cv2.VideoWriter('Lines.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_height, frame_width))  # fps at 20, decrease for accurate distance 
# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video stream or file")


color=0
motion= 'D'
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame= cv2.resize(frame, (frame_height, frame_width), interpolation = cv2.INTER_AREA)
            
        cx, cy, show, res = actual_pos(color, frame)

            
        show, dis, error = ref_line(color, motion, show, cx, cy)
        color, motion = control(color, motion, dis)
        
        text1 = f'Color of interest is {colors[color]}'
        text2 = f'Actual position of the body is  {cx}, {cy}'
        text3 = f'Distance left before next turn {round(dis, 3)}'
        text4 = f'Instantenous error in alignment is {round(error, 3)}'
        text5 = f'Motion of body is {motion}'
        
        cv2.putText(show, text1, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (52, 51, 50), 2) # 52, 51, 50
        cv2.putText(show, text2, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (52, 51, 50), 2) # 255, 255, 255
        cv2.putText(show, text3, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (52, 51, 50), 2)
        cv2.putText(show, text4, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (52, 51, 50), 2)
        cv2.putText(show, text5, (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (52, 51, 50), 2)
        
        out.write(show)
        cv2.imshow('Frame',show)
        cv2.imshow('HSV', res)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break



cap.release()
out.release()
cv2.destroyAllWindows()