import socket
import time
import final
import cv2
import initial
from findMarker import findMarker

PORT = [8001, 8002,8003,8004]
SOC= []
CLIENT= []

dictionary={}
# Use Mouse Click Event to initialise if you can 

# dictionary= {1:(0,0), 2:(0,0), 3:(0,0), 4:(0,0), 5:(0,0), 6:(0,0),
#             7:(0,0), 8:(0,0), 9:(0,0), 10:(0,0), 11:(0,0),
#             12:(0,0), 97:(0,0), 98:(0,0), 99:(0,0), 100:(0,0)}

for port in PORT:
    s= socket.socket()
    s.bind(('0.0.0.0', port ))
    s.listen(2)
    client, addr = s.accept()
    if not addr:
        time.sleep(5)
    content = client.recv(32)
    while True:
        if len(content) != 0:
            print(content)
            CLIENT.append(client)
            break 
        time.sleep(1)
    SOC.append(s)
bot= 0
throw= 250
cap= cv2.Videocapture('http://192.168.0.104.4747/video')

if (cap.isOpened()== False):
    print("Error opening video stream")


while(cap.isOpened()):
    ret, img = cap.read()
    if ret == True:
        dictionary= initial.first(img)
        break

while(cap.isOpened()):
    ret, img = cap.read()
    if ret == True:
        for i in range(1, 13):
            if findMarker(i, img)[0] != None:
                dictionary[i]= findMarker(i, img)
        for i in range(97, 101):
            if findMarker(i, img)[0] != None:
                dictionary[i]= findMarker(i, img)
        for client in CLIENT:
            speed= 1
            end=1
            bot+=1
            rev= False
            while(speed or end):
                _, img = cap.read()
                speed, direction, original, mask, end, dictionary = final.botdetails(bot, img, dictionary, rev=rev)
                client.send(speed.to_bytes(1, 'big'))
                time.sleep(0.07)
                client.send(direction.to_bytes(1, 'big'))
                time.sleep(0.07)
                if speed == 0 and end == 2:
                    rev= True
                    client.send(throw.to_bytes(1, 'big'))
                    time.sleep(0.07)
                    client.send(direction.to_bytes(1, 'big'))
                    time.sleep(0.07)
                    ## throw the thing
                    time.sleep(2)
                cv2.imshow("Original", original)
                cv2.imshow("Line to follow", mask)
    
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            client.close()
            time.sleep(1)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        
    else:
        break
