import numpy as np
from skimage.transform import hough_line, hough_line_peaks
import cv2
import time
from findMarker import findMarker
import warnings
warnings.filterwarnings('ignore')

BOT= [97, 98, 99, 100]

def checkNone(x, y, dictionary, id):
    if x is None or y is None:
        x, y= dictionary[id]
    return x, y

def angle(a1, b1, a2, b2, x, y, bot, rev):
    perp= line_to_point(a1, b1, a2, b2, x, y)
    if bot == 97 or bot == 98:
        perp= perp* -1
    hypt= distance(x, y, a2, b2)
    angle= np.arcsin(perp/hypt)
    angle= angle* 180/np.pi
    if angle <0:
        angle= 360- angle
    if not rev:
        return (angle*256)//360 - 1
    else:
        angle= 180- angle
        if angle< 0:
            angle= 360+ angle
        return (angle*256)//360 - 1

def line_to_point(a1, b1, a2, b2, x, y):
    num= (a2 - a1)*y + (b2- b1)*x - b1*(a2 - a1)+ a1*(b2 - b1)
    num= num/((a2 - a1)**2 + (b2 - b1)**2) **0.5
    return num

def distance(a1, b1, a2, b2):
    return ((a1-a2)**2 +(b1-b2)**2)**0.5

def create_mask(img, a1, b1, a2, b2):
    mask= np.zeros((img.shape[0], img.shape[1]))
    mask= cv2.line(mask, (a1, b1), (a2, b2), 255, 5, cv2.LINE_AA)
    image= cv2.line(img.copy(), (a1, b1), (a2, b2), (0, 0, 255), 5, cv2.LINE_AA)
    return mask, image

def destination(bot, img, x, y, dictionary, rev):
    x1, y1= findMarker(3*bot-2, img)
    x1, y1= checkNone(x1, y1, dictionary, 3*bot-2)
    dictionary[3*bot-2]= (x1, y1)
    x2, y2= findMarker(3*bot-1, img)
    x2, y2= checkNone(x2, y2, dictionary, 3*bot-1)
    dictionary[3*bot-1]= (x2, y2)
    x3, y3= findMarker(3*bot, img)
    x3, y3= checkNone(x3, y3, dictionary, 3*bot)
    dictionary[3*bot]= (x3, y3)

    if not rev:
        if(distance(x1,y1, x,y)* 1.15< distance(x3,y3,x,y)):
            mask, original= create_mask(img, x1, y1, x2, y2)
            theta= angle(x1, y1, x2, y2, x, y, bot, rev)
            return x2, y2, mask, original, theta, 1

        elif(distance(x1,y1, x,y)< distance(x3,y3,x,y)):
            destx, desty= (3*x+ 5*x2+ x3)/9, (3*y+ 5*y2+ y3)/9
            mask, original= create_mask(img, x, y, destx, desty)
            theta= angle(x2, y2, x3, y3, destx, desty, bot, rev)
            return destx, desty, mask, original, theta, 1

        else:
            mask, original= create_mask(img, x2, y2, x3, y3)
            theta= angle(x2, y2, x3, y3, x, y, bot, rev)
            return x3, y3, mask, original, theta, 2


    else:
        if(distance(x3,y3,x,y)* 1.15< distance(x1,y1,x,y)):
            mask, original= create_mask(img, x3, y3, x2, y2)
            theta= angle(x3, y3, x2, y2, x, y, bot, rev)
            return x2, y2, mask, original, theta, 1
        
        elif(distance(x3,y3,x,y) < distance(x1,y1,x,y)):
            destx, desty= (3*x+ 5*x2+ x1)/9, (3*y+ 5*y2+ y1)/9
            mask, original= create_mask(img, x, y, destx, desty)
            theta= angle(x2, y2, x1, y1, destx, desty, bot, rev)
            return destx, desty, mask, original, theta, 1

        else:
            mask, original= create_mask(img, x2, y2, x1, y1)
            theta= angle(x2, y2, x1, y1, x, y, bot, rev)
            return x1, y1, mask, original, theta, 0


def botdetails(bot, img, dictionary, rev=False):
    BOT= [97, 98, 99, 100]
    bot_id= BOT[bot-1]
    pos_x, pos_y= findMarker(bot_id, img)
    pos_x, pos_y = checkNone(pos_x, pos_y, dictionary, bot_id)
    dictionary[bot_id]= (pos_x, pos_y)
    dest_x, dest_y, mask, original, theta, end= destination(bot, img, pos_x, pos_y, dictionary, rev)
    speed=  distance(pos_x, pos_y, dest_x, dest_y)//300
    if speed >200:
        speed= 200
    if speed <5:
        speed = 5
    return speed, theta, original, mask, end, dictionary
