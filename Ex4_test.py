#This code demonstrate how to show location of hand landmark
import cv2
import mediapipe as mp

Nfing = ""
cap = cv2.VideoCapture(0)

#Call hand pipe line module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

fingerhigh=[4,8,12,16,20]
fingerbase=[3,7,11,15,19]
pong ="0"
chee="0"
glang="0"
nang="0"
goy="0"


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
                if id == 3:
                    id3 = int(id)
                    cx3 = cx
                #นิ้วโป้ง
                if id == 8:
                    id8 = int(id)
                    cx8 = cy
                if id == 7:
                    id7 = int(id)
                    cx7 = cy
                #นิ้วชี้
                if id == 12:
                    id12 = int(id)
                    cx12 = cy
                if id == 11:
                    id11 = int(id)
                    cx11 = cy
                #นิ้วกลาง
                if id == 16:
                    id16 = int(id)
                    cx16 = cy
                if id == 15:
                    id15 = int(id)
                    cx15 = cy
                #นิ้วนาง
                if id == 20:
                    id20 = int(id)
                    cy20 = cy
                    cx20 = cx
                if id == 19:
                    id19 = int(id)
                    cx19 = cy
                #นิ้วก้อย
    
        #for i in 
            if(cx20 < cx4):

                if (cx4 > cx3 ):
                    pong = "Pong "
                if (cx4 < cx3 ):
                    pong = ""
            elif(cx20 > cx4):

                if (cx4 < cx3 ):
                    pong = "Pong "
                if (cx4 > cx3 ):
                    pong = ""

            if (cx8 < cx7 ):
                chee = "Shee "
            if (cx8 > cx7 ):
                chee = ""

            if (cx12 < cx11 ):
                glang = "Klang "
            if (cx12 > cx11 ):
                glang = ""

            if (cx16 < cx15 ):
                nang = "Nang "
            if (cx16 > cx15 ):
                nang = ""

            if (cy20 < cx19 ):
                goy = "Koy"
            if (cy20 > cx19 ):
                goy = ""  

            Nfing = pong + chee + glang + nang + goy 
            
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    ID = "670610767"; 
    name ="Pom Lungpun"; 
    cv2.putText(img, str(int(ID)), (640-len(ID)*20, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                (27, 163, 3), 2)
    cv2.putText(img, str(name), (640-len(name)*20, 90), cv2.FONT_HERSHEY_PLAIN, 2,
                (27, 163, 3), 2)
    cv2.putText(img, str(str(Nfing)), (320-(len(Nfing) * 10), 450), cv2.FONT_HERSHEY_PLAIN, 2,(57, 255, 20), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
#Closeing all open windows
#cv2.destroyAllWindows()