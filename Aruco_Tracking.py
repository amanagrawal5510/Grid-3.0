import numpy as np
import cv2
import os
import cv2.aruco as aruco



def findArucoMarkers(img, markerSize=6,totalMarkers=250,draw=True):
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco, f"DICT_{markerSize}X{markerSize}_{totalMarkers}")
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    bbox,ids,rejected=aruco.detectMarkers(imgGray, arucoDict,parameters=arucoParam)

    if draw:
        aruco.drawDetectedMarkers(img,bbox)
    return [bbox,ids]

def augmentAruco(bbox,ids,img,imgAug,drawId=True):
    tl=bbox[0][0][0],bbox[0][0][1]
    tr=bbox[0][1][0],bbox[0][1][1]
    bl=bbox[0][2][0],bbox[0][2][1]
    br=bbox[0][3][0],bbox[0][3][1]

    h,w,c=imgAug.shape

    ptr1=np.array([tl,tr,bl,br])
    ptr2=np.float32([[0,0],[w,0],[w,h],[0,h]])
    matrix,_=cv2.findHomography(ptr2, ptr1)
    imgOut=cv2.warpPerspective(imgAug, matrix, (img.shape[1],img.shape[0]))
    cv2.fillConvexPoly(img, ptr1.astype(int), (0,0,0))
    imgOut=img+imgOut
    return imgOut

def main():
    cap=cv2.VideoCapture("Aruco Video.mp4")
    imgAug=cv2.imread("images/bad boys.png")
    while True:
        sucess, img=cap.read()
        arucoFound=findArucoMarkers(img)
        if len(arucoFound[0])!=0:
            for bbox,id in zip(arucoFound[0],arucoFound[1]):
                img=augmentAruco(bbox,id,img,imgAug,True)
        cv2.imshow("image",img)
        cv2.waitKey(1)

def imageAcroCode(file,markerSize=6,totalMarkers=250):
    img=cv2.imread(file)
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco, f"DICT_{markerSize}X{markerSize}_{totalMarkers}")
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    bbox,ids,rejected=aruco.detectMarkers(imgGray, arucoDict,parameters=arucoParam)
    print(bbox,ids)


if __name__=="__main__":
    imageAcroCode("droid1.png")