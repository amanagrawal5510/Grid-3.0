'''
AUTHOR: Aman Kanojiya
Call Function to get center Point or aruco
Parameters: Id, Image
Return: Center (If Found), None
'''

import cv2
import cv2.aruco as aruco


def findMarker(id, img, markerSize=6, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f"DICT_{markerSize}X{markerSize}_{totalMarkers}")
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(
        imgGray, arucoDict, parameters=arucoParam)
    for corner, i in zip(corners, ids):
        if int(id) == i:
            centerX = (corner[0][0][0] + corner[0][1][0] +
                       corner[0][2][0] + corner[0][3][0]) / 4
            centerY = (corner[0][0][1] + corner[0][1][1] +
                       corner[0][2][1] + corner[0][3][1]) / 4
            center = (int(centerX), int(centerY))
            return center
    else:
        return (None, None)


if __name__ == "__main__":
    img = cv2.imread("droid1.png")
    for i in range(1, 13):
        center_coordinates = findMarker(i, img)
        if center_coordinates[0] != None:
            img= cv2.putText(img, str(i), center_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 10, cv2.LINE_AA)
    for i in range(97, 101):
        center_coordinates = findMarker(i, img)
        if center_coordinates[0] != None:
            img= cv2.putText(img, str(i), center_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 10, cv2.LINE_AA)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(center_coordinates)