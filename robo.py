import cv2
import mediapipe as mp
import time
import pyfirmata

time.sleep(2.0)

mp_draw=mp.solutions.drawing_utils #use function drawing_utils to draw straight connect landmark point
mp_hand=mp.solutions.hands #use function hands to find hand on camera


tipIds=[4,8,12,16,20] # media-pipe position  of fingertips

L1=0
L2=0
L3=0
L4=0
L5=0
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
led_1=board.get_pin('d:13:o') #Set pin to output
led_2=board.get_pin('d:12:o')
led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')
led_5=board.get_pin('d:9:o')

#### LED write function

## controller.py ##

def showled(led_1,led_2,led_3,led_4,led_5,L1,L2,L3,L4,L5):#creat condition to controll digital out put
    led_1.write(L1)
    led_2.write(L2)
    led_3.write(L3)
    led_4.write(L4)
    led_5.write(L5)
######



video=cv2.VideoCapture(int(cport)) #OpenCamera at index position 0

with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:#(min_detection_confidence, min_tracking_confidence) are Value to considered for detect and tracking image
    while True:
        ret,image=video.read() #Read frame in camera video
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #convert color BGR to RGB
        image.flags.writeable=False  #to improve nothing drawed in image
        results=hands.process(image) #process image
        image.flags.writeable=True #can drawing  image
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  #convert color RGB to BGR
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])  #input number hand_landmark position and position of spot position hand_landmark
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)  #drawing hand skeleton from hand_landmark point
        fingers=[]
        if len(lmList)!=0:
            #Thumb check (LHS and RHS conditions) (x-position)
            if lmList[9][1]<lmList[5][1]:
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            #Other finger check (y-position)

            for id in range(1,5):
                # Normal condition
                if lmList[0][2]<lmList[5][2]: #creat condition for count fingers
                    if lmList[tipIds[id]][2] > lmList[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # Upside down
                else:
                    if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            led_1.write(fingers[0])
            led_2.write(fingers[1])
            led_3.write(fingers[2])
            led_4.write(fingers[3])
            led_5.write(fingers[4])
           
            #if ((results.multi_hand_landmarks))!="None":
             #   cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                
                #cv2.putText(image, , (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                #    2, (255, 0, 0), 5)
                
            #    cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
            #        2, (255, 0, 0), 5)
        cv2.imshow("Frame",image)  #show edited image
        k=cv2.waitKey(1)
        if k==ord('q'):  #press "q" to exit programe
            break
video.release()
cv2.destroyAllWindows()