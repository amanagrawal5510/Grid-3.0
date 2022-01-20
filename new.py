import cv2
import cv2.aruco as aruco

def findMarker(img, markerSize=6, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f"DICT_{markerSize}X{markerSize}_{totalMarkers}")
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(
        imgGray, arucoDict, parameters=arucoParam)
    cv2.aruco.drawDetectedMarkers(img, corners, ids, (0, 255, 0))
    cv2.imshow("image_", img)
    for corner, i in zip(corners, ids):
        # if int(id) == i:
        centerX = (corner[0][0][0] + corner[0][1][0] +
                       corner[0][2][0] + corner[0][3][0]) / 4
        centerY = (corner[0][0][1] + corner[0][1][1] +
                       corner[0][2][1] + corner[0][3][1]) / 4
        center = (int(centerX), int(centerY))
        return center
    else:
        return (None, None)


if __name__ == "__main__":
    cap = cv2.VideoCapture('http://192.168.0.104:4747/video')

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            findMarker(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
