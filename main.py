import numpy as np
import pyautogui as p
import pydirectinput
import keyboard
import tkinter as tk
import PIL
import cv2
import time

from PIL import ImageGrab
from pynput.mouse import Button, Controller
import threading

from detector import ImageDetector

p.useImageNotFoundException()


# Disable fail-safe
# p.FAILSAFE = False

class KnightBot:

    def __init__(self):
        self.detector = ImageDetector()
        self.misc_images, self.weapon_images = self.detector.register_images()
        # self.game_cycle()
        self.is_valuable_item_inv()

    def game_cycle(self):
        while True:
            if not self.is_genie_active():
                if self.is_bosalt_typed():
                    self.sell_items()
                    self.repair_items()

    def mouse_click(self, button, x, y, delay=0.1):
        p.moveTo(x, y)
        time.sleep(0.3)
        p.mouseDown(button=button)
        time.sleep(delay)
        p.mouseUp(button=button)

    def mouse_drag(self,button, x1, y1, x2, y2):
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
        try:
            p.locateOnScreen(
                "img/genie_play_button.jpg",
                confidence=0.95
            )
            return True
        except p.ImageNotFoundException:
            print("genie not active")
            return False

    def is_bosalt_typed(self):
        # bosalt text area tl230,630/br470,670
        try:
            p.locateOnScreen(
                "img/bosalt_text.jpg",
                confidence=0.6,
                region=(160, 615, 570, 720)
            )
            time.sleep(1)
            return True
        except p.ImageNotFoundException:
            time.sleep(1)
            return False

    def open_shop(self):
        self.press_esc()
        self.align_shop()
        self.mouse_click("left", 790, 700)
        # keyboard.press("space")
        self.mouse_click("right", 502, 500)
        time.sleep(2)
        try:
            loc = p.locateOnScreen(
                "img/tyroon_shop_big_pic.jpg",
                confidence=0.7
            )
            try:
                x_loc = p.locateCenterOnScreen(
                    "img/x_button.jpg",
                    confidence=0.7,
                    region=(max(loc[0] - 100, 0), max(0, loc[1] - 100), min(loc[0] + loc[2] + 100, 1024),
                            min(768, loc[1] + loc[3] + 100))
                )
                # print("searching x at:", (
                # max(loc[0] - 100, 0), max(0, loc[1] - 100), min(loc[0] + loc[2] + 100, 1024),
                # min(768, loc[1] + loc[3] + 100)))
                print("x_loc", x_loc)
                # if x_loc is None:
                #     self.openShop()
                return x_loc
            except p.ImageNotFoundException:
                print("x button not found")
                self.press_esc()
                return self.open_shop()
        except p.ImageNotFoundException:
            print("shop big pic not found")
            self.press_esc()
            return self.open_shop()

    def align_shop(self):
        self.key_press("b")
        p.moveTo(500, -1)
        time.sleep(2)

    def change_perspective(self):
        self.mouse_click("left", 790, 700)
        time.sleep(0.2)
        self.key_press("f9")
        time.sleep(0.2)

    def open_repair(self):
        x_loc = self.open_shop()
        # p.moveTo(ardin_text_location)
        # p.moveRel(0, 200)
        self.mouse_click("left", x_loc[0] - 50, x_loc[1] + 200)

    def open_trade(self):
        x_loc = self.open_shop()
        print("text_location", x_loc)
        self.mouse_click("left", x_loc[0] - 50, x_loc[1] + 170)
        time.sleep(2)
        self.mouse_click("left", 820, 310)
        self.mouse_click("left", 720, 550)
        p.moveTo(550, 500)

    def open_inventory(self):
        is_inventory_open = self.is_inventory_open()
        if is_inventory_open:
            print("inv is open")
        else:
            self.press_esc()
            self.key_press("I")

    def open_vip_inventory(self):
        try:
            self.open_inventory()
            self.mouse_click("left", 680, 340)
            time.sleep(1)
            p.locateOnScreen(
                "img/vip_inventory_identifier.jpg",
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
                "img/inventory_refresh_icon.jpg",
                confidence=0.7,
                region=(795, 355, 835, 395)
            )
            return True
        except p.ImageNotFoundException:
            return False

    def locate_items_in_inventory(self):

        # 680,440 inv ilk item 49-49 geçiş. 2 row, 7 col
        # check region tl290,0/br1000,520

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
        self.open_inventory()
        did_locate_all_items, item_coordinates, _ = self.locate_items_in_inventory()
        if did_locate_all_items:
            for item in item_coordinates:
                p.moveTo(item[0],item[1],1)
                time.sleep(1)
                is_valuable = self.is_valuable_item_inv()
                if is_valuable:
                    valuable_item_in_inv_coordinates.add(item)
            return item_coordinates-valuable_item_in_inv_coordinates, valuable_item_in_inv_coordinates
        else: print("error in locating all items in inventory")

    def locate_items_in_vip_inventory(self):

        # 315,80 vip ilk item 51-51 geçiş. 570,437 son item. 8 row, 6 col
        # check region  tl0,0/br620,530

        i = 0
        j = 0
        p.moveTo(790, 705)
        empty_slots = set()
        item_coordinates = set()
        while True:
            is_empty = p.pixelMatchesColor(
                320 + j * 51, 60 + i * 51, (25, 25, 25), 30
            )
            if not is_empty :
                item_coordinates.add((315 + j * 51, 80 + i * 51))
            else:
                empty_slots.add((315 + j * 51, 80 + i * 51))
            j += 1
            j = j % 6
            if j == 0:
                i += 1
                i = i % 8
            if len(item_coordinates) + len(empty_slots) == 48:
                return True, item_coordinates, empty_slots

    def locate_valuable_items_in_vip(self):
        valuable_item_in_vip_coordinates = set()
        self.open_vip_inventory()
        did_locate_all_items, item_coordinates, _ = self.locate_items_in_vip_inventory()
        if did_locate_all_items:
            for item in item_coordinates:
                p.moveTo(item[0],item[1],1)
                time.sleep(1)
                is_valuable = self.is_valuable_item_vip()
                if is_valuable:
                    valuable_item_in_vip_coordinates.add(item)
            return item_coordinates-valuable_item_in_vip_coordinates, valuable_item_in_vip_coordinates
        else: print("error in locating all items in inventory")

    def take_items_from_vip(self, vip_item_coordinates, inv_empty_slot):

        # 315,80 vip ilk item 51-51 geçiş. 570,437 son item. 8 row, 6 col
        # check region  tl0,0/br620,530

        items_to_take_count = min(len(vip_item_coordinates), inv_empty_slot)
        print("items:", vip_item_coordinates)
        for i in range(items_to_take_count):
            item = vip_item_coordinates.pop()
            p.moveTo(item[0],item[1],1)
            time.sleep(1)
            is_valuable = self.is_valuable_item_vip()
            if not is_valuable:
                self.mouse_click("right", item[0], item[1])
        self.mouse_click("left", 1000, 32)
        self.press_esc()

    def deposit_valuable_items_to_vip(self,valuable_items_inv,empty_slots_vip):
        #vip is already open, transform valuable item coords and drag to empty vip coords
        for item in range(len(valuable_items_inv)):
            self.mouse_drag("left",valuable_items_inv[item][0],valuable_items_inv[item][1],
                            empty_slots_vip[item][0],empty_slots_vip[item][1])

    def is_valuable_item_inv(self):
        # check region tl290,0/br1000,520
        detector = self.detector
        img = ImageGrab.grab(bbox=(0,0,1000,520))
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        print("entering loop")
        for template in self.weapon_images:
            detected, pos, located_precision = detector.locate_image_rgb(template[0],img_cv2,0.99)
            if detected:
                detector.detector_test(img_cv2,pos,template[1],template[2])
                cv2.imshow("item found", template[0])
                cv2.waitKey(0)
        return True

    def is_valuable_item_vip(self):
        # check region  tl0,0/br620,530
        return True

    def sell_items(self):
        while True:
            while True:
                time.sleep(1)
                self.open_trade()
                items_to_sell, valuable_items = self.locate_valuable_items_in_inv()
                for item in items_to_sell:
                    self.mouse_click("right",item[0], item[1])
                time.sleep(0.1)
                self.mouse_click("left",900, 460)
                time.sleep(0.5)
                self.mouse_click("left",725, 550)
                self.mouse_click("left",1000, 32)
                self.press_esc()
                time.sleep(1)
                _, items, empty_slots = self.locate_items_in_inventory()
                if len(empty_slots) + len(valuable_items) == 14:
                    break
            self.open_inventory()
            time.sleep(1)
            self.mouse_click("left",680, 340)
            # isVipFull = self.isVipInventoryFull()
            time.sleep(1)
            items_to_sell_vip, valuable_items_vip = self.locate_valuable_items_in_vip()
            self.take_items_from_vip(items_to_sell_vip, empty_slots)
            self.press_esc()
            time.sleep(0.2)
            _, items_vip, empty_slots_vip = self.locate_items_in_vip_inventory()
            if len(empty_slots_vip)>=len(valuable_items):
                self.deposit_valuable_items_to_vip(list(valuable_items),list(empty_slots_vip))
            if len(empty_slots_vip) + len(valuable_items_vip) == 48:
                break
        while True:
            time.sleep(0.4)
            self.open_trade()
            items_to_sell, valuable_items = self.locate_valuable_items_in_inv()
            for item in items_to_sell:
                self.mouse_click("right", item[0], item[1])
            time.sleep(0.1)
            self.mouse_click("left", 900, 460)
            time.sleep(0.5)
            self.mouse_click("left", 725, 550)
            self.mouse_click("left", 1000, 32)
            self.press_esc()
            time.sleep(1)
            _, items, empty_slots = self.locate_items_in_inventory()
            if len(empty_slots) + len(valuable_items) == 14:
                break
        self.change_perspective()
        self.change_perspective()
        self.change_perspective()

    def repair_items(self):

        # 645,270 inv bag open button
        # 480,420 bag ilk item 51-51 geçiş. 4 row, 3 col / 580,570 son item
        # repair coords, inv first 2 rows + coords below
        # 680,540 + 730,540 / 870,370 + 920,370 + 920,320 + 920,220 + 920,170 + 870,270

        self.open_repair()
        time.sleep(1)
        self.mouse_click("left", 645, 270)
        time.sleep(1)
        for i in range(4):
            for j in range(3):
                self.mouse_click("right",480+51*j,420+51*i)
        time.sleep(1)
        for i in range(2):
            for j in range(7):
                self.mouse_click("left",680 + j * 50, 340 + 50 * i)
        self.mouse_click("left",680,540)
        self.mouse_click("left",730,540)
        self.mouse_click("left",870,370)
        self.mouse_click("left",920,370)
        self.mouse_click("left",920,320)
        self.mouse_click("left",920,220)
        self.mouse_click("left",920,170)
        self.mouse_click("left",870,270)

        # fix coordinates

        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)

        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)

        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)

        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)
        self.mouse_drag("left",680,340,480,420)

        self.press_esc()

    def press_esc(self):
        time.sleep(0.1)
        self.key_press("esc")
        self.key_press("esc")
        self.key_press("esc")

bot = KnightBot()