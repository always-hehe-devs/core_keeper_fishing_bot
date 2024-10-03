from handlers.vision import Vision
import cv2 as cv
from handlers.capture import capture


def main():
    img_to_detect = Vision('./img/to_detect_2.png')
    while True:
        screenshot = capture("Core Keeper")

        img_to_detect.find(screenshot, 0.6)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
