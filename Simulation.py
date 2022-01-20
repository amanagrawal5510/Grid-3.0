'''
AUTHOR: Shreyansh Jain
Simple simulation of bot in top view
Background and initial position can be set depending on arena
'''

import cv2

__background = None
__width = None
__height = None
__markerOffset = None
__coords = []
__originalMarkers = []
__markers = []
__direction = []

def init(background, width, height, markerOffset):
    global __background,__width, __height, __markerOffset
    __background = background
    __markerOffset = markerOffset
    __width = width
    __height = height


def addVehicle(initialX, initialY, markerImage):
    global __coords, __markers, __originalMarkers
    __coords.append([
        [initialX-__width//2, initialY-__height//2],
        [initialX+__width//2, initialY+__height//2]
    ])
    markerImage = cv2.resize(markerImage,(__width - 2*__markerOffset, __height - 2*__markerOffset))
    __markers.append(markerImage)
    __originalMarkers.append(markerImage)
    __direction.append([0, 1])

def turn(vehicle_no, direction):
    global __direction, __markers
    if direction == 0:
        __markers[vehicle_no] = cv2.rotate(__originalMarkers[vehicle_no], cv2.ROTATE_180)
        __direction[vehicle_no] = [0, -1]
    elif direction == 1:
        __markers[vehicle_no] = cv2.rotate(__originalMarkers[vehicle_no], cv2.ROTATE_90_COUNTERCLOCKWISE)
        __direction[vehicle_no] = [1, 0]
    elif direction == 2:
        __markers[vehicle_no] = __originalMarkers[vehicle_no]
        __direction[vehicle_no] = [0, 1]
    elif direction == 3:
        __markers[vehicle_no] = cv2.rotate(__originalMarkers[vehicle_no], cv2.ROTATE_90_CLOCKWISE)
        __direction[vehicle_no] = [-1, 0]
        

def move(vehicle_no, speed):
    global __coords
    for i in range(2):
        for j in range(2):
            __coords[vehicle_no][i][j] += __direction[vehicle_no][j] * speed

def renderNextFrame():
    img = __background.copy()
    for i in range(len(__coords)):
        cv2.rectangle(img, __coords[i][0], __coords[i][1], (98, 136, 173), cv2.FILLED)
        img[
            (__coords[i][0][1]+__markerOffset):(__coords[i][1][1]-__markerOffset),
            (__coords[i][0][0]+__markerOffset):(__coords[i][1][0]-__markerOffset)
            ] = __markers[i]
    return img