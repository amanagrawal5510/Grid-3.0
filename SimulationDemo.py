import Simulation
import numpy as np
import cv2

backgroundMap = cv2.imread('Images/map.jpeg')
height, width, _ = backgroundMap.shape
backgroundSize = (width, height)
aruco_1 = cv2.imread('Images/aruco-1.png')
aruco_2 = cv2.imread('Images/aruco-2.png')
aruco_3 = cv2.imread('Images/aruco-3.png')
aruco_4 = cv2.imread('Images/aruco-4.png')

Simulation.init(backgroundMap, 50, 50, 10)
Simulation.addVehicle(538, 32, aruco_1)
Simulation.addVehicle(605, 32, aruco_2)
Simulation.addVehicle(674, 32, aruco_3)
Simulation.addVehicle(742, 32, aruco_4)

initialLocation = [[538, 32], [605, 32], [674, 32], [742, 32]]
finalLocation = [[43, 573], [43, 641], [1236, 641], [1236, 573]]
midPoints = [[538, 573], [605, 641], [674, 641], [742, 573]]
stepSize = 5

currentIndex = 0
pathStatus = 0

def getMidpoints(corners):
    return int(sum([x[0] for x in corners])//4), int(sum([x[1] for x in corners])//4)

def detectAcro(id, image):
    corners, ids, _ = cv2.aruco.detectMarkers(image, cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50))
    outputImage = cv2.aruco.drawDetectedMarkers(image, corners, ids)
    return getMidpoints(corners[np.where(ids == id)[0][0]][0]), outputImage

def performMovement(centerCoords):
    global pathStatus, currentIndex

    step = 0
    turn = -1
    if pathStatus == 0:
        step = abs(centerCoords[1] - midPoints[currentIndex][1])
        if currentIndex < 2:
            turn = 3
        else:
            turn = 1
    elif pathStatus == 1:
        step = abs(centerCoords[0] - finalLocation[currentIndex][0])
        if currentIndex < 2:
            turn = 1
        else:
            turn = 3
    elif pathStatus == 2:
        step = abs(centerCoords[0] - midPoints[currentIndex][0])
        turn = 0
    elif pathStatus == 3:
        step = abs(centerCoords[1] - initialLocation[currentIndex][1])
    

    if step <= stepSize:
        Simulation.move(currentIndex, step)
        Simulation.turn(currentIndex, turn)
        pathStatus += 1
        if pathStatus == 4:
            pathStatus = 0
            currentIndex += 1
    else:
        Simulation.move(currentIndex, stepSize)


def refLine(centerCoords, image):
    if pathStatus == 0:
        cv2.line(image, centerCoords, midPoints[currentIndex],(0,255,0),2)
        cv2.line(image, finalLocation[currentIndex], midPoints[currentIndex],(0,255,0),2)
    elif pathStatus == 1:
        cv2.line(image, centerCoords, finalLocation[currentIndex],(0,255,0),2)
    elif pathStatus == 2:
        cv2.line(image, centerCoords, midPoints[currentIndex],(0,255,0),2)
        cv2.line(image, initialLocation[currentIndex], midPoints[currentIndex],(0,255,0),2)
    elif pathStatus == 3:
        cv2.line(image, centerCoords, initialLocation[currentIndex],(0,255,0),2)
    return image


def cvProcessor(image):
    # process image
    # then move / turn the required vehicle
    # by using Simulation.move or Simulation.turn
    # Simulation.move(vehicle index (0 based indexing), pixels to move)
    # Simulation.turn(vehicle index (0 based indexing), direction to turn (0-top, 1-right, 2-bottom, 3-left))

    centerCoords, outputImage = detectAcro(currentIndex+1, image)
    outputImage = refLine(centerCoords, outputImage)
    performMovement(centerCoords)
    return outputImage

result = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, backgroundSize)

while True:
    if currentIndex == 4:
        break
    current_frame = Simulation.renderNextFrame()
    out = cvProcessor(current_frame)
    cv2.imshow('frame', out)
    result.write(out)
    if cv2.waitKey(50) & 0xff == ord('q'):
        break
result.release()