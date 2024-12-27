import cv2
import mediapipe as mp
import time
from pyfirmata import Arduino, SERVO, util

time.sleep(2.0)

mp_draw = mp.solutions.drawing_utils 
mp_hand = mp.solutions.hands  

tipIds = [4, 8, 12, 16, 20] 

def check_user_input(input):
    try:
        
        val = int(input)
        bv = True
    except ValueError:
        try:
           
            val = float(input)
            bv = True
        except ValueError:
            bv = False
    return bv

#### SERVO function control ####

def rotateservo(pin, angle): 
    board.digital[pin].write(angle)
    #time.sleep(0.015)


cport = input('Enter the camera port: ')
while not check_user_input(cport):
    print('Please enter a number, not a string')
    cport = input('Enter the camera port: ')

comport = input('Enter the Arduino board COM port: ')
while not check_user_input(comport):
    print('Please enter a number, not a string')
    comport = input('Enter the Arduino board COM port: ')

# เชื่อมต่อกับ Arduino
board = Arduino('COM' + comport)
pin = 9
board.digital[pin].mode = SERVO  # กำหนดให้ pin 9 เป็นโหมด SERVO

# เปิดกล้อง
video = cv2.VideoCapture(int(cport))

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read() 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        image.flags.writeable = False  
        results = hands.process(image)
        image.flags.writeable = True  
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
        total_fingers_count = 0  

        # ตรวจจับหลายมือ
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                fingers = [] 
                lmList = []
                for id, lm in enumerate(hand_landmark.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])  
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)  

              
                if len(lmList) != 0:
                   
                    if lmList[9][1] < lmList[5][1]:
                        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    else:
                        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    for id in range(1, 5):
                        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    total_fingers_count += fingers.count(1)
                    rotateservo(9,total_fingers_count*18)      
            ID = "670610767"
            cv2.putText(image, f"{total_fingers_count}", (45, 375),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            cv2.putText(image,str(ID), (440, 70), cv2.FONT_HERSHEY_PLAIN, 2,(27, 163, 3), 2)
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):  
            break

video.release()
cv2.destroyAllWindows()
