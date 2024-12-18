import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

# Call hand pipeline module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

finger_tips = [4, 8, 12, 16, 20]   # ปลายนิ้ว
finger_bases = [3, 7, 11, 15, 19]  # โคนของนิ้ว
finger_status = [0] * 5            # เก็บสถานะของแต่ละนิ้ว

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # เก็บตำแหน่ง landmark ทั้งหมด
            landmarks = []
            h, w, c = img.shape
            for lm in handLms.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))

            # ตรวจสอบสถานะของนิ้ว
            for i in range(5):
                tip_id = finger_tips[i]
                base_id = finger_bases[i]
                if i == 0:  # นิ้วโป้ง (ตรวจสอบตามแนวนอน)
                    finger_status[i] = 1 if landmarks[tip_id][0] > landmarks[base_id][0] else 0
                else:       # นิ้วอื่น (ตรวจสอบตามแนวตั้ง)
                    finger_status[i] = 1 if landmarks[tip_id][1] < landmarks[base_id][1] else 0

            # คำนวณจำนวนที่นิ้วชูขึ้น
            Nfing = sum(finger_status)

            # วาดเส้นเชื่อมต่อบนมือ
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # แสดงจำนวนบนหน้าจอ
    cv2.putText(img, str(int(Nfing)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
