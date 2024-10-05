from handlers.vision import Vision
import cv2 as cv
from handlers.capture import CaptureScreen


def main():
    img_to_detect = Vision('./img/to_detect_2.png')
    capture = CaptureScreen("Core Keeper")
    print("Process running...")
    while True:
        screenshot = capture.capture_screen()

        img_to_detect.find(screenshot, 0.6, debug_mode="rectangles")

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
        capture.release()


if __name__ == '__main__':
    main()
