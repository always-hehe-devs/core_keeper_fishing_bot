import cv2 as cv
import numpy as np
import pyautogui
import time


class Vision:

    def __init__(self, img_to_detect, method=cv.TM_CCOEFF_NORMED):
        self.img_to_detect = cv.imread(img_to_detect, cv.IMREAD_UNCHANGED)

        self.img_to_detect_w = self.img_to_detect.shape[1]
        self.img_to_detect_h = self.img_to_detect.shape[0]
        self.method = method

    def find(self, screenshot, threshold=0.6, debug_mode=None):
        result = cv.matchTemplate(screenshot, self.img_to_detect, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.nonzero(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.img_to_detect_w, self.img_to_detect_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, _ = cv.groupRectangles(rectangles, groupThreshold=2, eps=0.5)

        points = []
        if len(rectangles):
            print('Found img.')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            for (x, y, w, h) in rectangles:

                center_x = x + int(w/2)
                center_y = y + int(h/2)
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    haystack_img = np.array(screenshot, copy=True)
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, thickness=2, lineType=line_type)

                target_x = center_x
                target_y = center_y + 350  # Where to click? Calculate?

                pyautogui.moveTo(target_x, target_y)
                pyautogui.mouseDown(button='right')
                time.sleep(1.5)
                pyautogui.mouseUp(button='right')

        if debug_mode:
            cv.imshow('Debug', screenshot)

        return points
