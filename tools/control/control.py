from tools import pydirectinputplus as pdi
from tools.dict import *
import pyautogui as pag
import random as rnd
import numpy as np
import time
import cv2


# 無存檔快速截圖 方便比對 回傳cv2格式的灰度圖片
def get_screenshot():
    # pyautogui獲取截圖後 用numpy將RGB陣列轉換為BGR陣列 .cv2.cvtColor(image,cv2.COLOR_BGRA2GRAY) 將圖片轉換為灰度圖像
    return cv2.cvtColor(np.array(pag.screenshot())[:, :, ::-1],cv2.COLOR_BGRA2GRAY)

# 讀取圖片 回傳cv2格式的灰度圖片
def read_image(image_path):
    return cv2.imread("screenshots/" + image_path, cv2.IMREAD_GRAYSCALE)

# 比對圖片 回傳cv2格式的match值
def match(screenshot, temp):
    return cv2.matchTemplate(screenshot, temp, cv2.TM_CCOEFF_NORMED)

# 查找並點擊
def find_and_click(image_path, alt=False, xOffset=0, yOffset=0, try_times_limit=-1, thresold=0.8, interrupt=None, found=None, try_time_gap = 1):
    global action_thread_stop, Log_print
    # 加載要查找的圖像
    temp = read_image(image_path)
    try_times = 0
    while True:
        try_times += 1
        if action_thread_stop[0] :
            if interrupt != None : interrupt[0] = True
            if found != None : found[0] = True
            return
        Log_print[0](f'正在尋找 {image_path} 第 {try_times} 次...')
        # 獲取屏幕截圖
        screenshot = get_screenshot()
        # 使用模板匹配定位圖像
        result = match(screenshot, temp)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        if maxVal >= thresold:
            top_left = maxLoc
            h, w = temp.shape

            # 目標座標
            target_x = top_left[0] + w // 2 + xOffset
            target_y = top_left[1] + h // 2 + yOffset

            if(alt): pdi.keyDown("alt")

            pdi.moveTo(x=target_x, y=target_y, duration=rnd.uniform(0.35, 0.75))

            pdi.click()
            
            if(alt): pdi.keyUp("alt")
            if(found!=None) : found[0] = True
            break
        else:
            if((try_times_limit != -1) and (try_times >= try_times_limit)):
                if(interrupt != None) : interrupt[0] = True
                break
            time.sleep(try_time_gap)

# 拖曳
def drag(startX=None, startY=None, endX=None, endY=None):
    pdi.moveTo(x=startX, y=startY, duration=rnd.uniform(0.35, 0.75))
    pdi.mouseDown(button=pdi.LEFT)
    pdi.moveTo(x=endX, y=endY, duration=rnd.uniform(0.35, 0.75))
    pdi.mouseUp(button=pdi.LEFT)

# 根據圖片相對拖曳
def dragRelPic(image_path, xOffset=0, yOffset=0, thresold=0.9):
    temp = read_image(image_path)
    while True:
        global action_thread_stop
        if action_thread_stop[0] : 
            return
        screenshot = get_screenshot()
        result = match(screenshot, temp)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        if(maxVal >= thresold):
            
            top_left = maxLoc
            h, w = temp.shape

            target_x = top_left[0] + w // 2
            target_y = top_left[1] + h // 2

            pdi.moveTo(x=target_x, y=target_y, duration=rnd.uniform(0.35, 0.75))

            pdi.mouseDown(button=pdi.LEFT)
            pdi.moveTo(x=target_x+xOffset, y=target_y+yOffset, duration=rnd.uniform(0.35, 0.75))
            pdi.mouseUp(button=pdi.LEFT)

            break
        else:
            print("finding...", image_path)
            time.sleep(1)