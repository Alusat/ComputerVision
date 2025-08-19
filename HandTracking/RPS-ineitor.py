import math
import cv2
import time
from HandTrackingModule import HandDetector


def main(showInfo=False):
    pTime = 0

    camera_indexes = [-1,0, 1, 2, 3, 4]
    cap = None

    for index in camera_indexes:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        time.sleep(0.5)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera found at index {index}")
                break
            else:
                cap.release()
                cap = None
        else:
            cap = None

    if cap is None:
        print("Error: Could not access any camera!")
        return

    detector = HandDetector(
        static_image_mode=False,
        maxHands=1,  # maximo 1 mano para jugar piedrapapeltijera
        modelComplexity=1,
        minDetectionConfidence=0.7,
        minTrackingConfidence=0.5
    )

    currentRPS = "???"
    RPS_indicator = None

    # cargar imágenes
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
        if not success:
            break

        drawLines = True
        img = detector.findHands(img, drawLines)

        drawDots = False
        lmList = detector.findPosition(img, 0, drawDots)

        # Crea ventana RPS
        if RPS_indicator is None:
            cv2.imshow("RPS Indicator", unknown_img)
            RPS_indicator = True

        if len(lmList) == 0:
            currentRPS = "???"
            RPS_winning_img = unknown_img.copy()
        else:
            cx, cy = lmList[12][1], lmList[12][2]  # corazón
            ix, iy = lmList[8][1], lmList[8][2]    # índice
            lengthCI = math.hypot(cx - ix, cy - iy)

            px, py = lmList[4][1], lmList[4][2]   # pulgar
            mx, my = lmList[20][1], lmList[20][2] # meñique
            lengthPM = math.hypot(px - mx, py - my)

            lengthPI = math.hypot(px - ix, py - iy)

            bmx, bmy = lmList[0][1], lmList[0][2] # base palma
            lengthBmBc = math.hypot(bmx - cx, bmy - cy)

            if lengthCI > lengthPM:
                RPS_winning_img = rock_img.copy()
                currentRPS = "SCISSORS"
            elif lengthPM > 3 * lengthCI and lengthPI > lengthCI:
                RPS_winning_img = scissors_img.copy()
                currentRPS = "PAPER"
            elif lengthPM < lengthBmBc:
                RPS_winning_img = paper_img.copy()
                currentRPS = "ROCK"
            else:
                RPS_winning_img = unknown_img.copy()
                currentRPS = "???"

        # actualizar siempre RPS
        cv2.imshow("RPS Indicator", RPS_winning_img)

        # solo para debug
        if showInfo:
            if len(lmList) > 0:
                cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)
                cv2.circle(img, (ix, iy), 15, (255, 255, 0), cv2.FILLED)
                cv2.line(img, (cx, cy), (ix, iy), (255, 255, 0), 2)

                cv2.circle(img, (px, py), 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (mx, my), 15, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (px, py), (mx, my), (255, 0, 0), 2)

                cv2.circle(img, (ix, iy), 15, (0, 255, 0), cv2.FILLED)
                cv2.line(img, (px, py), (ix, iy), (0, 255, 0), 2)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f"FPS: {int(fps)}", (10, 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            cv2.imshow("Hand Tracking", img)

        # detectar teclas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('i'):
            showInfo = not showInfo
            if not showInfo:
                cv2.destroyWindow("Hand Tracking")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
