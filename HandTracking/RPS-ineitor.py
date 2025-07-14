import math
import cv2
import numpy as np
import time
from HandTrackingModule import HandDetector


def main(showInfo=True):  # info para debugear
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector(
        static_image_mode=False,
        maxHands=1,  #maximo 1 mano para jugar piedrapapeltijera
        modelComplexity=1,
        minDetectionConfidence=0.7,
        minTrackingConfidence=0.5
    )

    currentRPS = "???"
    RPS_indicator = None

    while True:
        success, img = cap.read()
        if not success:  # si no hay camara nada
            break

        drawLines = True
        img = detector.findHands(img, drawLines)

        drawDots = False  # puntos + grandes
        lmList = detector.findPosition(img, 0, drawDots)  # ya deja los valres en pixeles

        # Create RPS indicator window (always active)
        if RPS_indicator is None:
            RPS_indicator_img = np.zeros((200, 400, 3), np.uint8)
            cv2.imshow("RPS Indicator", RPS_indicator_img)
            RPS_indicator = True

        # Update RPS indicator content
        RPS_indicator_img = np.zeros((200, 400, 3), np.uint8)
        if len(lmList) == 0:
            currentRPS = "???"
            RPSinator_text = "???"
        else:
            # mirar libreria de mediapipe para saber que indices corresponden a cada dedo
            cx, cy = lmList[12][1], lmList[12][2]  # x y de la punta del dedo corazón
            ix, iy = lmList[8][1], lmList[8][2]  # x y de la punta del dedo indice
            lengthCI = math.hypot(cx - ix, cy - iy)  # dist corazón indice

            px, py = lmList[4][1], lmList[4][2]  # x y de la punta del dedo pulgar
            mx, my = lmList[20][1], lmList[20][2]  # x y de la punta del dedo meñique
            lengthPM = math.hypot(px - mx, py - my)  # dist pulgar meñique

            lengthPI = math.hypot(px - ix, py - iy)  # dist pulgar indice

            bmx, bmy = lmList[0][1], lmList[0][2] # x y de la base de la palma
            bcx, bcy = lmList[9][1], lmList[9][2]
            lengthBmBc = math.hypot(bmx - cx, bmy - cy) # distancia base mano-base corazon

            if lengthCI > lengthPM:
                currentRPS = "SCISSORS"
                RPSinator_text = "ROCK WINS!"
            elif lengthPM > 3 * lengthCI and lengthPI > lengthCI:
                currentRPS = "PAPER"
                RPSinator_text = "SCISSORS WINS!"
            elif lengthPM < lengthBmBc:
                currentRPS = "ROCK"
                RPSinator_text = "PAPER WINS!"
            else:
                currentRPS = "???"
                RPSinator_text = "???"


        # Always update the RPS indicator window
        cv2.putText(RPS_indicator_img, f"Your move: {currentRPS}", (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(RPS_indicator_img, RPSinator_text, (50, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("RPS Indicator", RPS_indicator_img)

        if showInfo:
            if len(lmList) > 0:
                cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)
                cv2.circle(img, (ix, iy), 15, (255, 255, 0), cv2.FILLED)
                cv2.line(img, (cx, cy), (ix, iy), (255, 255, 0), 2)
                print("corazon-indice")
                print(lengthCI)

                cv2.circle(img, (px, py), 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (mx, my), 15, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (px, py), (mx, my), (255, 0, 0), 2)
                length = math.hypot(px - mx, py - my)
                print("pulgar-meñique")
                print(lengthPM)

                cv2.circle(img, (ix, iy), 15, (0, 255, 0), cv2.FILLED)
                cv2.line(img, (px, py), (ix, iy), (0, 255, 0), 2)
                print("pulgar-indice")
                print(lengthPI)

            cv2.imshow("Hand Tracking", img)  # mostrar ventana con imagen
            print(currentRPS)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if showInfo:
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            cv2.imshow("Hand Tracking", img)  # mostrar ventana con imagen

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()