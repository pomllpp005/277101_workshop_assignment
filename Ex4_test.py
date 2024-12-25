#This code demonstrate how to show location of hand landmark
import cv2
import mediapipe as mp

Nfing = ""
cap = cv2.VideoCapture(0)

#Call hand pipe line module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
L1=0
L2=0
L3=0
L4=0
L5=0


import time
import pyfirmata

time.sleep(2.0)


def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        # print("Input is an integer number. Number = ", val)
        bv = True
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            # print("Input is a float  number. Number = ", val)
            bv = True
        except ValueError:
            # print("No.. input is not a number. It's a string")
            bv = False
    return bv

cport = input('Enter the camera port: ')
while not (check_user_input(cport)):
    print('Please enter a number not string')
    cport = input('Enter the camera port: ')

comport = input('Enter the arduino board COM port: ')
while not (check_user_input(comport)):
    print('Please enter a number not string')
    comport = input('Enter the arduino board COM port: ')

board=pyfirmata.Arduino('COM'+comport)
led_1=board.get_pin('d:12:o') #Set pin to output
led_2=board.get_pin('d:11:o')
led_3=board.get_pin('d:10:o')
led_4=board.get_pin('d:9:o')
led_5=board.get_pin('d:8:o')

#### LED write function

## controller.py ##

def led(led_1,led_2,led_3,led_4,led_5,L1,L2,L3,L4,L5):#creat condition to controll digital out put
        led_1.write(L1)
        led_2.write(L2)
        led_3.write(L3)
        led_4.write(L4)
        led_5.write(L5)
    




    

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 4:
                    id4 = int(id)
                    cx4 = cx
                    cy4 = cy
                if id == 3:
                    id3 = int(id)
                    cx3 = cx
                    cy3 = cy
                    
                #นิ้วโป้ง
                if id == 8:
                    id8 = int(id)
                    cy8 = cy
                    cx8 = cx
                if id == 7:
                    id7 = int(id)
                    cy7 = cy
                    cx7 = cx
                #นิ้วชี้
                if id == 12:
                    id12 = int(id)
                    cx12 = cx
                    cy12 = cy
                if id == 11:
                    id11 = int(id)
                    cy11 = cy
                    cx11 = cx
                #นิ้วกลาง
                if id == 16:
                    id16 = int(id)
                    cy16 = cy
                    cx16 = cx
                if id == 15:
                    id15 = int(id)
                    cy15 = cy
                    cx15 = cx
                #นิ้วนาง
                if id == 20:
                    id20 = int(id)
                    cy20 = cy
                    cx20 = cx
                if id == 19:
                    id19 = int(id)
                    cy19 = cy
                    cx19 = cx
                #นิ้วก้อย
    
        #for i in 
            if(cx20 < cx4):

                if (cx4 > cx3 ):
                    L1 = 1
                if (cx4 < cx3 ):
                    L1 = 0
            elif(cx20 > cx4):

                if (cx4 < cx3 ):
                    L1 = 1
                if (cx4 > cx3 ):
                    L1 = 0
            if (cy8 < cy7 ):
                L2 = 1
            if (cy8 > cy7 ):
                L2 = 0

            if (cy12 < cy11 ):
                L3 = 1
            if (cy12 > cy11 ):
                L3 = 0

            if (cy16 < cy15 ):
                L4 = 1
            if (cy16 > cy15 ):
                L4 = 0

            if (cy20 < cy19 ):
                L5 = 1
            if (cy20 > cy19 ):
                L5 = 0
            led(led_1,led_2,led_3,led_4,led_5,L1,L2,L3,L4,L5)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    ID = "670610767"; 
    name ="Pom Lungpun"; 
    cv2.putText(img, str(int(ID)), (640-len(ID)*20, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                (27, 163, 3), 2)
    cv2.putText(img, str(name), (640-len(name)*20, 90), cv2.FONT_HERSHEY_PLAIN, 2,
                (27, 163, 3), 2)
    #cv2.putText(img, str(str(Nfing)), (320-(len(Nfing) * 10), 450), cv2.FONT_HERSHEY_PLAIN, 2,(57, 255, 20), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
#Closeing all open windows
#cv2.destroyAllWindows()