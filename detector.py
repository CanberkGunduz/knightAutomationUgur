import time, pyautogui
import cv2
import numpy as np
from PIL import ImageGrab, Image
from pathlib import Path

class ImageDetector:

    # TEST FUNCTION #
    def detector_test(self, screen, l, w, h):
        topLeft = (l[0], l[1])
        bottomRight = (l[0] + h, l[1] + w)
        cv2.rectangle(screen, topLeft, bottomRight, (0, 0, 255), 2)
        cv2.circle(screen, center=(int(l[0] + h / 2), int(l[1] + w / 2)), radius=1, color=(0, 0, 255), thickness=5)
        # cv2.circle(screen, center=(int(l[0] + h/2), int(l[1] + w/2)), radius=1, color=(0,0,255), thickness=5)
        cv2.imshow("imageDetector", screen)
        cv2.waitKey(0)

    # TEMPLATE DETECTOR #
    def templateDetector_fullscreen(self, path, threshold=0.9):
        detected = False
        target = cv2.imread(r"{}".format(path))
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        w, h = target.shape[::][0], target.shape[::][1]
        screen = np.array(pyautogui.screenshot())
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        results = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(results)
        if round(maxVal, 2) >= threshold: detected = True
        print(f"{path}: {detected}, {round(maxVal, 2)}")
        self.detector_test(screen, maxLoc, w, h)
        return detected, maxLoc, w, h

    def templateDetector_rgb(self, path, x=0, y=0, sw=1032, sh=800, threshold=0.9):
        detected = False
        target = cv2.imread(r"{}".format(path))
        w, h = target.shape[::][0], target.shape[::][1]
        screen = cv2.cvtColor(np.array(pyautogui.screenshot(region=(x, y, sw, sh))), cv2.COLOR_BGR2RGB)
        results = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(results)
        if round(maxVal, 2) >= threshold: detected = True
        print(f"{path}: {detected}, {round(maxVal, 2)}")
        self.detector_test(screen, maxLoc, w, h)
        return detected, maxLoc, w, h

    def templateDetector_gry(self, path, x=0, y=0, sw=1032, sh=800, threshold=0.9):
        detected = False
        target = cv2.imread(r"{}".format(path))
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        w, h = target.shape[::][0], target.shape[::][1]
        screen = np.array(pyautogui.screenshot(region=(x, y, sw, sh)))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        results = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(results)
        if round(maxVal, 2) >= threshold: detected = True
        print(f"{path}: {detected}, {round(maxVal, 2)}")
        self.detector_test(screen, maxLoc, w, h)
        return detected, maxLoc, w, h

    def templateDetector_hsv(self, path, x=0, y=0, sw=1032, sh=800, threshold=0.9):
        detected = False
        target = cv2.imread(r"{}".format(path))
        target = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
        w, h = target.shape[::][0], target.shape[::][1]
        screen = np.array(pyautogui.screenshot(region=(x, y, sw, sh)))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        results = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(results)
        if round(maxVal, 2) >= threshold: detected = True
        print(f"{path}: {detected}, {round(maxVal, 2)}")
        self.detector_test(screen, maxLoc, w, h)
        return detected, maxLoc, w, h

    def locate_image_rgb(self, template,img_cv2,precision = 0.9):
        res = cv2.matchTemplate(img_cv2, template, cv2.TM_CCOEFF_NORMED)
        min_val, located_precision, min_loc, pos = cv2.minMaxLoc(res)
        print(located_precision,pos)
        detected = False
        if located_precision > precision: detected = True
        return detected, pos, located_precision,

    def register_images(self):
        misc_img_names = ["bosalt_text","genie_play_button_off","genie_play_button_on",
                          "inventory_refresh_icon","inventory_text","shop_big_pic","tyroon_shop_big_pic",
                          "vip_chest_icon","vip_inventory_identifier","warehouse_text","x_button"]
        weapon_img_names = ["chitin_text","iron_bow","large_breaker_4_mp","large_breaker_6",
                            "large_breaker_6_mp","mp_recovery_text","sword_breaker_4_mp",
                            "tomahawk_5_hp","tomahawk_5_mp"]
        weapon_images = []
        misc_images = []
        for name in misc_img_names:
            target = cv2.imread(f"images/misc/{name}.jpg")
            width, height = target.shape[::][0], target.shape[::][1]
            misc_images.append((target,width,height))

        for name in weapon_img_names:
            target = cv2.imread(f"images/weapons/{name}.jpg")
            width, height = target.shape[::][0], target.shape[::][1]
            weapon_images.append((target,width,height))

        print(f"{len(weapon_images)} {len(misc_images)}")
        return misc_images, weapon_images


# a = ImageDetector()
# a.detector_test(screen = np.array(pyautogui.screenshot(region=(0, 0, 1920, 1080))),l=(100,100),w=100,h=100)
# a.templateDetector_fullscreen("img/youtube_text.jpg")
# a.templateDetector_rgb("img/youtube_text.jpg")
# a.templateDetector_hsv("img/youtube_text.jpg")