import numpy as np
import pyautogui as p
import keyboard
import cv2
import time
from PIL import ImageGrab

p.useImageNotFoundException()

# Disable fail-safe
p.FAILSAFE = False


class KnightBot:

    def __init__(self):
        self.detector = ImageDetector()
        self.misc_images = self.detector.register_images()
        self.game_cycle()

    def game_cycle(self):
        while True:
            time.sleep(5)
            if not self.is_genie_active():
                print("genie not active")
                if self.is_bosalt_typed():
                    print("bosalt typed")
                    self.repair_items()
                    time.sleep(600)

    def mouse_click(self, button, x, y, delay=0.1):
        p.moveTo(x, y)
        time.sleep(0.3)
        p.mouseDown(button=button)
        time.sleep(delay)
        p.mouseUp(button=button)

    def mouse_drag(self, button, x1, y1, x2, y2):
        p.moveTo(x1, y1)
        time.sleep(0.1)
        p.mouseDown(button=button)
        time.sleep(0.05)
        p.moveTo(x2, y2, 1)
        time.sleep(0.05)
        p.mouseUp(button=button)

    def key_press(self, key, delay=0.3):
        time.sleep(0.1)
        keyboard.press(key)
        time.sleep(delay)
        keyboard.release(key)

    def is_genie_active(self):
        detector = self.detector
        img = ImageGrab.grab(bbox=(200, 0, 460, 150))
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        template = self.misc_images[1]
        detected, pos, located_precision = detector.locate_image_rgb(template, img_cv2, 0.9)
        return not detected

    def is_bosalt_typed(self):
        detector = self.detector
        img = ImageGrab.grab(bbox=(180, 620, 430, 700))
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        template = self.misc_images[0]
        detected, pos, located_precision = detector.locate_image_rgb(template, img_cv2, 0.8)
        return detected

    def open_shop(self):
        self.press_esc()
        self.align_shop()
        self.mouse_click("left", 790, 700)
        self.mouse_click("right", 502, 500)
        time.sleep(1)
        try:
            loc = p.locateOnScreen(
                "images/misc/tyroon_shop_big_pic.jpg",
                confidence=0.7
            )
            try:
                x_loc = p.locateCenterOnScreen(
                    "images/misc/x_button.jpg",
                    confidence=0.7,
                    region=(max(loc[0] - 100, 0), max(0, loc[1] - 100), min(loc[0] + loc[2] + 100, 1024),
                            min(768, loc[1] + loc[3] + 100))
                )

                return x_loc
            except p.ImageNotFoundException:
                self.press_esc()
                return self.open_shop()
        except p.ImageNotFoundException:
            self.press_esc()
            return self.open_shop()

    def align_shop(self):
        self.mouse_click("left", 790, 700)
        self.key_press("b")
        p.moveTo(500, -1)
        time.sleep(1)

    def open_repair(self):
        x_loc = self.open_shop()
        self.mouse_click("left", x_loc[0] - 50, x_loc[1] + 200)

    def repair_items(self):
        self.open_repair()

        self.mouse_click("left", 680, 540)
        self.mouse_click("left", 870, 370)
        self.mouse_click("left", 920, 370)
        self.mouse_click("left", 920, 320)
        self.mouse_click("left", 920, 220)
        self.mouse_click("left", 920, 170)
        self.mouse_click("left", 870, 270)

        self.press_esc()

    def press_esc(self):
        time.sleep(0.1)
        self.key_press("esc")
        self.key_press("esc")
        self.key_press("esc")


class ImageDetector:

    def locate_image_rgb(self, template, img_cv2, precision=0.9):
        res = cv2.matchTemplate(img_cv2, template[0], cv2.TM_CCOEFF_NORMED)
        min_val, located_precision, min_loc, pos = cv2.minMaxLoc(res)
        print(template[3], located_precision, pos)
        detected = False
        if located_precision > precision:
            detected = True
        return detected, pos, located_precision,

    def register_images(self):
        misc_img_names = ["bosalt_text", "genie_play_button_off", "genie_play_button_on",
                          "inventory_refresh_icon", "inventory_text", "shop_big_pic", "tyroon_shop_big_pic",
                          "vip_chest_icon", "vip_inventory_identifier", "warehouse_text", "x_button","monster_stone_text"]

        misc_images = []
        for name in misc_img_names:
            target = cv2.imread(f"images/misc/{name}.jpg")
            width, height = target.shape[::][0], target.shape[::][1]
            misc_images.append((target, width, height, name))

        return misc_images


bot = KnightBot()
