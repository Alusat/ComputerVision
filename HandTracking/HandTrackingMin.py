import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #camara


mpHands = mp.solutions.hands

static_image_mode = False #track and detect dependiendo del nivel de confianza
#si es static siempre detectar (será mas lento)
maxHands = 1
modelComplexity = 1
minDetectionConfidence = 0.5
minTrackingConfidence = 0.5
hands = mpHands.Hands(static_image_mode,maxHands, modelComplexity, minDetectionConfidence, minTrackingConfidence)

mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()


    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks: #si se detecta algo
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)  #numero id del punto, pos x en pixeles, pos y en pixeles
                #cv2.circle(img, (int(cx), int(cy)), 20, (255, 0, 255), cv2.FILLED)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,30),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)