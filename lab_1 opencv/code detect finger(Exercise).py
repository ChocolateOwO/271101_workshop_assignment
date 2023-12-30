#This code demonstrate how to show location of hand landmark
import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0)
#Call hand pipe line module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

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
                if id == 8:
                    id8 = int(id)
                    cy8 = cy 
                if id == 7:
                    id7 = int(id)
                    cy7 = cy 
                if id == 6:
                    id6 = int(id)
                    cy6 = cy   
                if id == 12:
                    id12 = int(id)
                    cy12 = cy   
                if id == 10:
                    id10 = int(id)
                    cy10 = cy     
                if id == 16:
                    id16 = int(id)
                    cy16 = cy  
                if id == 15:
                    id15 = int(id)
                    cy15 = cy    
                if id == 20:
                    id20 = int(id)
                    cy20 = cy   
                if id == 18:
                    id18 = int(id)
                    cy18 = cy  

            if cy20 < cy18:
                cv2.putText(img, "Little finger is showing", (10, 200), cv2.FONT_HERSHEY_PLAIN, 1.5,(49, 229, 238), 2)
            if cy16 < cy15:
                cv2.putText(img, "Ring finger is showing", (10, 250), cv2.FONT_HERSHEY_PLAIN, 1.5,(160, 100, 224), 2)
            if cy12 < cy10:
               cv2.putText(img, "Middle finger is showing", (10, 300), cv2.FONT_HERSHEY_PLAIN, 1.5,(231, 44, 143), 2)
            if cy8 < cy7:
                cv2.putText(img, "Index finger is showing ", (10, 350), cv2.FONT_HERSHEY_PLAIN, 1.5,(231, 146, 44), 2)
            if cx3 < cx4:
                cv2.putText(img, "Thumb is showing ", (10, 400), cv2.FONT_HERSHEY_PLAIN, 1.5,(44, 231, 50), 2)


            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.putText(img, "Nidchima Boonkhwan-660610829", (200, 450), cv2.FONT_HERSHEY_PLAIN, 1.6, (156, 246, 139), 3)

    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
#Closeing all open windows
#cv2.destroyAllWindows()