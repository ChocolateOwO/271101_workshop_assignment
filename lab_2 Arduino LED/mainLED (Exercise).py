## mainLED.py ##

import cv2
import mediapipe as mp
import time
import pyfirmata

time.sleep(2.0)

mp_draw=mp.solutions.drawing_utils #use function drawing_utils to draw straight connect landmark point
mp_hand=mp.solutions.hands #use function hands to find hand on camera
cap = cv2.VideoCapture(0)
mpHands = mp_hand.Hands()
mpDraw = mp_draw

tipIds=[4,8,12,16,20] # media-pipe position  of fingertips

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

board = pyfirmata.Arduino('COM' + comport)
led_pins = [board.get_pin(f'd:{pin}:o') for pin in [13, 12, 11, 10, 9]]
# รวมอาเรย์ช่องพอร์ตของอาร์ดูโน่ไว้จะได้ไม่ต้องเขียนยาวๆ led_pins สร้างไว้สำหรับเก็บข้อมูลหลอดไฟที่เราเก็บไว้ตามช่องพอร์ตของอาร์ดูโน่ 13, 12, 11, 10, 9  
def led(fingers):
    for idx, pin in enumerate(led_pins):
        if fingers[idx] == 1:
            pin.write(1) # ทำให้สั้นลงเลขหนึ่งคือถ้านิ้วที่เก็บมา ตรวจสอบนิ้วจาก fingers ถ้ามีก็เเสดงไฟให้ขึ้นตามตำแหน่งนิ้วนั้น
        else:
            pin.write(0) # ถ้าไม่มีให้ปิดไฟดวงอื่นที่ไม่ได้แสดงหรือนิ้วไม่ได้อยู่ในลิสของ fingers

#idx = index คือตำแหน่งนิ้วที่เก็บไว้ในอาเรย์ ของenumerate(led_pins)
#enumerate ห็เหมือนอาร์เรย์ในภาษาซี ที่จะเก็บข้อมูลไว้ใช้ในกรณีที่เรียกมา ตรงนี้ข้อมูลที่เก็บจะเป้นหมาเลข led_pins
            ####



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
            #print(lmList[9],lmList[5])
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
            for id in range(1,5): 
                if lmList[0][2]<lmList[5][2]: #creat condition for count fingers
                    if lmList[tipIds[id]][2] > lmList[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)         
            total=fingers.count(1)
            
            led(fingers) #import function in module to control arduino output
            """
            creat condition to put text in frame

            """
            if ((results.multi_hand_landmarks))!="None":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, str(total), (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)

                    
        cv2.imshow("Frame",image)  #show edited image
        k=cv2.waitKey(1)
        if k==ord('q'):  #press "q" to exit programe
            break
video.release()
cv2.destroyAllWindows()