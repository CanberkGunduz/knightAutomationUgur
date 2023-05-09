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
        self.misc_images, self.weapon_images, self.mp_text = self.detector.register_images()
        self.game_cycle()

    def game_cycle(self):
        while True:
            time.sleep(5)
            if not self.is_genie_active():
                print("genie not active")
                if self.is_bosalt_typed():
                    print("bosalt typed")
                    time.sleep(3)
                    self.sell_items()
                    self.deposit_all_to_vip()
                    self.repair_items()
                    self.ts_scroll()
                    time.sleep(1)
                    self.ts_scroll()
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
        img = ImageGrab.grab(bbox=(660, 0, 840, 80))
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

    def open_trade(self):
        x_loc = self.open_shop()
        self.mouse_click("left", x_loc[0] - 50, x_loc[1] + 170)
        time.sleep(1)
        self.mouse_click("left", 820, 310)
        self.mouse_click("left", 720, 550)
        p.moveTo(550, 500)

    def open_inventory(self):
        is_inventory_open = self.is_inventory_open()
        if not is_inventory_open:
            self.press_esc()
            self.key_press("I")

    def open_vip_inventory(self):
        try:
            self.open_inventory()
            self.mouse_click("left", 680, 340)
            time.sleep(1)
            p.locateOnScreen(
                "images/misc/vip_inventory_identifier.jpg",
                confidence=0.7,
                region=(630, 75, 980, 240)
            )
        except p.ImageNotFoundException:
            time.sleep(0.1)
            self.press_esc()
            self.open_vip_inventory()

    def is_inventory_open(self):
        p.moveTo(510, 410)
        try:
            p.locateOnScreen(
                "images/misc/inventory_refresh_icon.jpg",
                confidence=0.7,
                region=(795, 355, 835, 395)
            )
            print("inventory is open")
            return True
        except p.ImageNotFoundException:
            print("inventory is closed")
            return False

    def open_bag(self):
        is_open = self.is_bag_open()
        if not is_open:
            self.mouse_click("left", 645, 270)

    def is_bag_open(self):
        p.moveTo(790, 700)
        try:
            p.locateOnScreen(
                "images/misc/bag_icon.jpg",
                confidence=0.7,
                region=(500, 300, 560, 355)
            )
            return True
        except p.ImageNotFoundException:
            return False

    def locate_items_in_inventory(self):
        i = 0
        j = 0
        p.moveTo(790, 705)
        empty_slots = set()
        item_coordinates = set()
        while True:
            is_empty = p.pixelMatchesColor(
                680 + j * 49, 421 + i * 49, (25, 25, 25), 30
            )
            if not is_empty:
                item_coordinates.add((680 + j * 49, 440 + i * 49))
            else:
                empty_slots.add((680 + j * 49, 440 + i * 49))
            j += 1
            j = j % 7
            if j == 0:
                i += 1
                i = i % 2
            if len(item_coordinates) + len(empty_slots) == 14:
                return True, item_coordinates, empty_slots

    def locate_valuable_items_in_inv(self):
        valuable_item_in_inv_coordinates = set()
        did_locate_all_items, item_coordinates, _ = self.locate_items_in_inventory()
        if did_locate_all_items:
            for item in item_coordinates:
                p.moveTo(item[0], item[1], 0.1)
                # time.sleep(0.3)
                is_valuable = self.is_valuable_item_inv()
                if is_valuable:
                    valuable_item_in_inv_coordinates.add(item)
            print(item_coordinates.difference(valuable_item_in_inv_coordinates), valuable_item_in_inv_coordinates)
            return item_coordinates.difference(valuable_item_in_inv_coordinates), valuable_item_in_inv_coordinates
        else:
            print("error in locating all items in inventory")

    def locate_items_in_vip_inventory(self):
        i = 0
        j = 0
        p.moveTo(790, 705)
        empty_slots = set()
        item_coordinates = set()
        while True:
            is_empty = p.pixelMatchesColor(
                320 + j * 51, 60 + i * 51, (25, 25, 25), 30
            )
            if not is_empty:
                item_coordinates.add((315 + j * 51, 80 + i * 51))
            else:
                empty_slots.add((315 + j * 51, 80 + i * 51))
            j += 1
            j = j % 6
            if j == 0:
                i += 1
                i = i % 7
            if len(item_coordinates) + len(empty_slots) == 42:
                return True, item_coordinates, empty_slots

    def locate_valuable_items_in_vip(self):
        valuable_item_in_vip_coordinates = set()
        did_locate_all_items, item_coordinates, _ = self.locate_items_in_vip_inventory()
        if did_locate_all_items:
            for item in item_coordinates:
                p.moveTo(item[0], item[1], 0.1)
                is_valuable = self.is_valuable_item_vip()
                if is_valuable:
                    valuable_item_in_vip_coordinates.add(item)
            print(item_coordinates.difference(valuable_item_in_vip_coordinates), valuable_item_in_vip_coordinates)
            return item_coordinates.difference(valuable_item_in_vip_coordinates), valuable_item_in_vip_coordinates
        else:
            print("error in locating all items in vip")

    def take_items_from_vip(self, vip_item_coordinates, inv_empty_slot):
        items_to_take_count = min(len(vip_item_coordinates), len(inv_empty_slot))

        for i in range(items_to_take_count):
            item = vip_item_coordinates.pop()
            self.mouse_click("right", item[0], item[1])

    def deposit_valuable_items_to_vip(self, valuable_items_inv):
        for item in valuable_items_inv:
            self.mouse_click("right", item[0] - 12, item[1] - 62)

    def deposit_all_to_vip(self):
        self.open_vip_inventory()
        for i in range(2):
            for j in range(7):
                self.mouse_click("right", 665 + 50 * j, 380 + 50 * i)
        self.press_esc()

    def is_valuable_item_inv(self):
        detector = self.detector
        img = ImageGrab.grab(bbox=(290, 0, 1000, 520))
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        mp_detected, mp_pos, mp_located_precision = detector.locate_image_rgb(self.mp_text, img_cv2, 0.9)
        for template_index in range(len(self.weapon_images)):
            if template_index < 3:
                detected, pos, located_precision = detector.locate_image_rgb(self.weapon_images[template_index],
                                                                             img_cv2, 0.95)
                if detected and mp_detected:
                    print("valuable item")
                    return True
            else:
                detected, pos, located_precision = detector.locate_image_rgb(self.weapon_images[template_index],
                                                                             img_cv2, 0.95)
                if detected:
                    print("valuable item")
                    return True
        return False

    def is_valuable_item_vip(self):
        detector = self.detector
        img = ImageGrab.grab(bbox=(0, 0, 620, 530))
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        mp_detected, mp_pos, mp_located_precision = detector.locate_image_rgb(self.mp_text, img_cv2, 0.9)
        for template_index in range(len(self.weapon_images)):
            if template_index < 3:
                detected, pos, located_precision = detector.locate_image_rgb(self.weapon_images[template_index],
                                                                             img_cv2, 0.95)
                if detected and mp_detected:
                    print("valuable item")
                    return True
            else:
                detected, pos, located_precision = detector.locate_image_rgb(self.weapon_images[template_index],
                                                                             img_cv2, 0.95)
                if detected:
                    print("valuable item")
                    return True
        return False

    def monster_stone(self):
        bag2_empty_slots=[]
        detector = self.detector

        self.mouse_click("left",550,380)

        for i in range(4):
            for j in range(3):
                x=480 + 51 * j
                y=420 + 51 * i
                if p.pixelMatchesColor(x,y,(0,0,0),30):
                    bag2_empty_slots.append((x,y))

        # print(bag2_empty_slots)

        _, items, _ = self.locate_items_in_inventory()

        for item in items:
            p.moveTo(item[0],item[1],0.1)
            img = ImageGrab.grab(bbox=(290, 0, 1000, 520))
            img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            ms_detected, ms_pos, ms_located_precision = detector.locate_image_rgb(self.misc_images[-1], img_cv2, 0.9)
            if ms_detected:
                if len(bag2_empty_slots)>0:
                    empty_slot = bag2_empty_slots.pop()
                    self.mouse_drag("left",item[0],item[1],empty_slot[0],empty_slot[1])
                else:
                    self.mouse_drag("left", item[0], item[1], 970,370)
                    self.mouse_click("left",755,395)

        self.mouse_click("left",485,380)

    def ts_scroll(self):
        self.mouse_click("left",20,490)
        self.mouse_click("left",55,490)
        time.sleep(0.5)
        self.mouse_click("left",915, 115)
        self.mouse_click("left",890, 545)
        time.sleep(0.5)
        self.mouse_click("left",430, 440)

        self.press_esc()


    def sell_items(self):
        self.open_inventory()
        time.sleep(1)
        self.monster_stone()
        while True:
            while True:
                time.sleep(1)
                self.open_inventory()
                items_to_sell, valuable_items = self.locate_valuable_items_in_inv()
                self.open_trade()
                for item in items_to_sell:
                    self.mouse_click("right", item[0] - 14, item[1] + 112)
                time.sleep(0.1)
                self.mouse_click("left", 900, 460)
                time.sleep(0.5)
                self.mouse_click("left", 725, 550)
                self.mouse_click("left", 1000, 32)
                self.press_esc()
                time.sleep(1)
                self.open_inventory()
                _, items, empty_slots = self.locate_items_in_inventory()
                if len(empty_slots) + len(valuable_items) == 14:
                    print("inventory emptied")
                    break
            self.open_vip_inventory()
            time.sleep(1)
            items_to_sell_vip, valuable_items_vip = self.locate_valuable_items_in_vip()
            self.take_items_from_vip(items_to_sell_vip, empty_slots)
            _, items_vip, empty_slots_vip = self.locate_items_in_vip_inventory()
            if len(empty_slots_vip) >= len(valuable_items):
                self.deposit_valuable_items_to_vip(list(valuable_items))
            self.press_esc()
            time.sleep(0.2)
            if len(empty_slots_vip) + len(valuable_items_vip) == 42:
                print("vip emptied")
                break
        while True:
            time.sleep(0.4)
            self.open_inventory()
            items_to_sell, valuable_items = self.locate_valuable_items_in_inv()
            self.open_trade()
            for item in items_to_sell:
                self.mouse_click("right", item[0] - 14, item[1] + 112)
            time.sleep(0.1)
            self.mouse_click("left", 900, 460)
            time.sleep(0.5)
            self.mouse_click("left", 725, 550)
            self.mouse_click("left", 1000, 32)
            self.press_esc()
            time.sleep(1)
            self.open_inventory()
            _, items, empty_slots = self.locate_items_in_inventory()
            if len(empty_slots) + len(valuable_items) == 14:
                break

    def repair_items(self):
        self.open_inventory()
        time.sleep(1)
        self.open_bag()
        time.sleep(1)
        for i in range(4):
            for j in range(3):
                self.mouse_click("right", 480 + 51 * j, 420 + 51 * i)
        time.sleep(1)
        self.open_repair()
        for _ in range(2):
            for i in range(2):
                for j in range(7):
                    self.mouse_click("left", 680 + j * 50, 440 + 50 * i)
            self.mouse_click("left", 680, 540)
            self.mouse_click("left", 870, 370)
            self.mouse_click("left", 920, 370)
            self.mouse_click("left", 920, 320)
            self.mouse_click("left", 920, 220)
            self.mouse_click("left", 920, 170)
            self.mouse_click("left", 870, 270)

        self.press_esc()
        self.open_inventory()

        self.mouse_drag("left", 680, 440, 480, 420)
        self.mouse_drag("left", 720, 440, 530, 420)
        self.mouse_drag("left", 770, 440, 580, 420)

        self.mouse_drag("left", 820, 440, 480, 470)
        self.mouse_drag("left", 870, 440, 530, 470)
        self.mouse_drag("left", 920, 440, 580, 470)

        self.mouse_drag("left", 970, 440, 480, 520)
        self.mouse_drag("left", 680, 490, 530, 520)
        self.mouse_drag("left", 720, 490, 580, 520)

        self.mouse_drag("left", 770, 490, 480, 570)
        self.mouse_drag("left", 820, 490, 530, 570)
        self.mouse_drag("left", 870, 490, 580, 570)

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
        weapon_img_names = ["large_breaker_4",
                            "large_breaker_6", "sword_breaker_4",
                            "tomahawk_5", "chitin_text", "iron_bow_text", ]
        weapon_images = []
        misc_images = []
        for name in misc_img_names:
            target = cv2.imread(f"images/misc/{name}.jpg")
            width, height = target.shape[::][0], target.shape[::][1]
            misc_images.append((target, width, height, name))

        for name in weapon_img_names:
            target = cv2.imread(f"images/weapons/{name}.jpg")
            width, height = target.shape[::][0], target.shape[::][1]
            weapon_images.append((target, width, height, name))

        target = cv2.imread(f"images/misc/mp_text.jpg")
        width, height = target.shape[::][0], target.shape[::][1]
        mp_text = (target, width, height, "mp_text")
        print(f"{len(weapon_images)} {len(misc_images)}")
        return misc_images, weapon_images, mp_text


bot = KnightBot()
