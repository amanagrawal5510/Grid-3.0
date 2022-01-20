import socket
import time

PORT = [8080, 8060,8040,8020]
SOC=[]
CLIENT=[]
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

# s = socket.socket()
# s.bind(('0.0.0.0', PORT ))
# s.listen(1)
# arr=''

for client in CLIENT:
    
    tic= time.time()

    tac= time.time()
    print(f'Forward motion started with {tac-tic} initial sec')
    i=1
    while(tac- tic <5):
        if(tac-tic <i):
            print(f'Forward motion started with {tac-tic} initial sec')
            i+=1
        tac= time.time()
        if(tac-tic == 1 or tac-tic == 2 or tac-tic == 3 or tac-tic == 4):
            print(f'Forward motion started with {tac-tic} initial sec with speed {int((5-(tac-tic))*2)}')
        speed= int((5-(tac-tic))*50)
        if speed < 0:
            speed= 0
        elif speed >254:
            speed = 254
        direction = 0
        client.send(speed.to_bytes(1, 'big'))
        time.sleep(0.1)
        client.send(direction.to_bytes(1, 'big'))
        time.sleep(0.1)
    
    tic= time.time()
    tac= time.time()
    print(f'Backward motion started with {tac-tic} initial sec')
    i=1
    while(tac- tic <5):
        if(tac-tic <i):
            print(f'Backward motion started with {tac-tic} initial sec')
            i+=1
        tac= time.time()
        if(tac-tic == 1 or tac-tic == 2 or tac-tic == 3 or tac-tic == 4):
            print(f'Backward motion started with {tac-tic} initial sec with speed {int((5-(tac-tic))*2)}')
        speed= int((5-(tac-tic))*50)
        if speed < 0:
            speed= 0
        elif speed >254:
            speed = 254
        direction = 63
        client.send(speed.to_bytes(1, 'big'))
        time.sleep(0.1)
        client.send(direction.to_bytes(1, 'big'))
        time.sleep(0.1)

    client.close()
    time.sleep(1)	


# while True:
#     client, addr = s.accept()
#     if not addr:
#         time.sleep(5)
#     else:
#     #to be added into ipbots client and address
#         while True:
#             content = client.recv(32)
#             if len(content) == 0:
#                 break
#             else:
#                 print(content)
#             while True:
#                 a = input().split(' ')
#                 for obj in a :
#                     arr+= chr(int(obj))
#                 client.send(arr.encode('ascii'))
#                 arr=''

#     print("Closing connection")
#     client.close()
