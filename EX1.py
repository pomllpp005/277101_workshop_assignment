import cv2

cap = cv2.VideoCapture(0)  # เปิดกล้อง

while True:
    success, img = cap.read()
    if not success:
        break

    # อ่านขนาดของจอ
    h, w, c = img.shape
    print(f"Width: {w}, Height: {h}")

    # แสดงข้อความต่ำสุดและสูงสุดบนจอ
    cv2.putText(img, f"Min: (0, 0)", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(img, f"Max: ({w-1}, {h-1})", (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # กด 'q' เพื่อออกจากโปรแกรม
        break

cap.release()
cv2.destroyAllWindows()
