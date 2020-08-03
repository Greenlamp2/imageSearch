import time
import numpy as np
import cv2


import pyautogui
from PIL import ImageGrab, Image


class ImageSearch:
    def __init__(self):
        self.timesample = 1

    def cut_region(self, region):
        x1 = region[0]
        y1 = region[1]
        width = region[2] - x1
        height = region[3] - y1

        return pyautogui.screenshot(region=(x1, y1, width, height))

    def imagesearch(self, image, precision=0.8):
        im = pyautogui.screenshot()
        im.save('testarea.png')
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        return max_loc

    def imagesearchAll(self, image, precision=0.8):
        im = pyautogui.screenshot()
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        ret = []
        for pt in zip(*loc[::-1]):
            ret.append((pt[0], pt[1]))
        return ret

    def get_region(self, path, pos):
        template = cv2.imread(path, 0)
        height, width = template.shape
        x1 = pos[0]
        y1 = pos[1]

        x2 = x1 + width
        y2 = y1 + height

        return x1, y1, x2, y2

    def getShape(self, path):
        template = cv2.imread(path, 0)
        return template.shape


    def lookup(self, path, loop=True):
        pos = self.imagesearch(path)
        while loop and pos[0] == -1:
            print(path + " not found, waiting")
            time.sleep(self.timesample)
            pos = self.imagesearch(path)
        return pos

    def lookAll(self, path):
        pos = self.imagesearchAll(path, 0.6)
        return pos

    def roi(self, img, vertices):
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, 255)
        masked = cv2.bitwise_and(img, mask)
        return masked

    def draw_lines(self, img, lines):
        try:
            for line in lines:
                coords = line[0]
                cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3)
        except:
            pass

    def process_img(self, original_image, regions):
        processed_img = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
        for region in regions:
            pts1 = region[0]
            pts2 = region[1]
            processed_img = cv2.rectangle(processed_img, pts1, pts2, color=(0, 255, 0), thickness=2)
        return processed_img

    def live(self, path):
        height, width = self.getShape(path)
        while True:
            screen = np.array(ImageGrab.grab())
            pos = self.lookAll(path)
            print(len(pos))
            regions = []
            if pos:
                for p in pos:
                    x1 = p[0]
                    y1 = p[1]
                    x2 = x1 + width
                    y2 = y1 + height

                    regions.append(((x1, y1), (x2, y2)))
            new_screen = self.process_img(screen, regions)
            new_screen = cv2.resize(new_screen, (1680, 1050))
            cv2.imshow('window', new_screen)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
