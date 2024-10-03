from time import time
from handlers.vision import Vision
import cv2 as cv
from handlers.capture import capture


def main():
    vision_limestone = Vision('./img/to_detect_2.png')
    loop_time = time()
    while True:
        screenshot = capture("Core Keeper")

        vision_limestone.find(screenshot, 0.6, debug_mode='rectangles')

        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
