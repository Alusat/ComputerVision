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

    #cargar imagnes
    rock_img = cv2.imread("images/rock.png")
    paper_img = cv2.imread("images/paper.png")
    scissors_img = cv2.imread("images/scissors.png")
    unknown_img = cv2.imread("images/unknown.png")

    # que tengan todas el mismo tamaño
    rock_img = cv2.resize(rock_img, (800, 1000))
    paper_img = cv2.resize(paper_img, (800, 1000))
    scissors_img = cv2.resize(scissors_img, (800, 1000))
    unknown_img = cv2.resize(unknown_img, (800, 1000))

    while True:
        success, img = cap.read()
        if not success:  # si no hay camara nada
            break

        drawLines = True
        img = detector.findHands(img, drawLines)

        drawDots = False  # puntos + grandes
        lmList = detector.findPosition(img, 0, drawDots)  # ya deja los valres en pixeles

        # Crea ventana RPS
        if RPS_indicator is None:
            #RPS_winning_img = np.zeros((200, 400, 3), np.uint8)
            cv2.imshow("RPS Indicator", unknown_img)
            RPS_indicator = True

        # Actualizar valor actula de RPS
        #RPS_winning_img = np.zeros((200, 400, 3), np.uint8)
        if len(lmList) == 0:
            currentRPS = "???"
            RPS_winning_img = unknown_img.copy()

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
            lengthBmBc = math.hypot(bmx - cx, bmy - cy) # distancia base mano-base corazon

            if lengthCI > lengthPM:
                RPS_winning_img = rock_img.copy()
                currentRPS = "SCISSORS"
                # RPSinator_text = "ROCK WINS!"

            elif lengthPM > 3 * lengthCI and lengthPI > lengthCI:
                RPS_winning_img = scissors_img.copy()
                currentRPS = "PAPER"
                # RPSinator_text = "SCISSORS WINS!"

            elif lengthPM < lengthBmBc:
                RPS_winning_img = paper_img.copy()
                currentRPS = "ROCK"
                # RPSinator_text = "PAPER WINS!"

            else:
                RPS_winning_img = unknown_img.copy()
                currentRPS = "???"
                # RPSinator_text = "???"

        # actualizar siempre RPS
        # Eliminado el texto superpuesto sobre la imagen
        cv2.imshow("RPS Indicator", RPS_winning_img)

        #solo para debugear
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
                print("pulgar-meñique")
                print(lengthPM)

                cv2.circle(img, (ix, iy), 15, (0, 255, 0), cv2.FILLED)
                cv2.line(img, (px, py), (ix, iy), (0, 255, 0), 2)
                print("pulgar-indice")
                print(lengthPI)

            cv2.imshow("Hand Tracking", img)  # mostrar ventana con imagen
            print(currentRPS)

        #salir con q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #calcular fps y mostrar camara
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
