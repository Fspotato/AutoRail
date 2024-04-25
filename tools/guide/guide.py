from tools import pydirectinputplus as pdi
from tools import control as ctrl
from tools.dict import *
import time

# 自動戰鬥
def autobattle(times:int=1, hit=False, repByFuel=False, repByStellar=False):
    global action_thread_stop
    if action_thread_stop[0] : return
    if (times < 1) : raise ValueError("times can only greater or equal than 1")
    ctrl.find_and_click(BATTLE_START)
    if (autoReplenish(repByFuel=repByFuel, repByStellar=repByStellar)) : ctrl.find_and_click(BATTLE_START)
    ctrl.find_and_click(BATLLE_REAL_START)
    if(hit):
        time.sleep(2.5)
        pdi.click()
    for _ in range(times-1):
        ctrl.find_and_click(AGAIN, thresold=0.85, try_time_gap=10)
        if (autoReplenish(repByFuel=repByFuel, repByStellar=repByStellar)) : ctrl.find_and_click(AGAIN, thresold=0.85, try_time_gap=10)
        time.sleep(1.5)
    time.sleep(2)
    ctrl.find_and_click(EXIT_BATTLE, try_time_gap=10)

# 自動補充開拓力
def autoReplenish(repByFuel=False, repByStellar=False):
    global action_thread_stop
    if action_thread_stop[0] : return
    if(repByFuel == False and repByStellar == False) : return False
    found = [False]
    ctrl.find_and_click(POWER_REPLENISH, try_times_limit=3, found=found)
    if (not found[0]) : return False
    if (repByFuel):
        found = [False]
        ctrl.find_and_click(FUEL, try_times_limit=3, found=found)
        if (not found[0]) :
            raise Exception("沒有燃料可以使用了!")
        ctrl.find_and_click(CONFIRM)
        time.sleep(0.5)
        ctrl.find_and_click(CONFIRM)
        ctrl.find_and_click(SPACE_CLOSE)
        return True
    return False

# 收集每日獎勵
def claim_daily_reward():
    global action_thread_stop
    if action_thread_stop[0] : return

    ctrl.find_and_click(GUIDE, alt=True, thresold=0.75)
    ctrl.find_and_click(DAILY_REWARD, try_times_limit=3)

    interrupt = [False]
    for _ in range(5):
        if(interrupt[0]):break
        ctrl.find_and_click(CLAIM_DAILY_REWARD, try_times_limit=3, interrupt=interrupt)
        time.sleep(0.5)
    
    interrupt = [False]
    ctrl.find_and_click(CLAIM_ALL_DAILY_REWARD, try_times_limit=3, thresold=0.9, interrupt=interrupt)
    if(not interrupt[0]) : ctrl.find_and_click(SPACE_CLOSE)

    ctrl.find_and_click(CLOSE)

# 擬造花萼
def flower_battle(color, times, target, place=None):
    global action_thread_stop
    if action_thread_stop[0] : return

    if target in [_.value for _ in CrimsonFlowerText]:
        target = [_.value for _ in CrimsonFlower][[_.value for _ in CrimsonFlowerText].index(target)]

    if target in [_.value for _ in GoldenFlowerText] :
        target = [_.value for _ in GoldenFlower][[_.value for _ in GoldenFlowerText].index(target)]

    if place in [_.value for _ in PlaceText] :
        place = [_.value for _ in Place][[_.value for _ in PlaceText].index(place)]

    ctrl.find_and_click(GUIDE, True, thresold=0.75)
    ctrl.find_and_click(SURVIVAL, try_times_limit=3)

    if color == GOLDEN_FLOWER_TEXT : 
        ctrl.find_and_click(GOLDEN_FLOWER)
        ctrl.find_and_click(place, try_times_limit=3)
        ctrl.find_and_click("calyx/" + target, xOffset=540, yOffset=5)
    elif color == CRIMSON_FLOWER_TEXT :
        ctrl.find_and_click(CRIMSON_FLOWER)
        found = [False]
        while True:
            ctrl.find_and_click("calyx/" + target, xOffset = 350, try_times_limit=2, thresold=0.9, found=found, try_time_gap=0.33)
            if found[0] : break
            ctrl.dragRelPic(CREDIT, yOffset=-250)
            time.sleep(0.5)

    ctrl.find_and_click(BATTLE_START, xOffset=100, yOffset=-70, humanlike=False)
    autobattle(times, repByFuel=False)

# 凝滯虛影
def stagnant_shadow_battle(image_path, times=1, repByFuel=False):
    global action_thread_stop
    if action_thread_stop[0] : return

    if image_path in [_.value for _ in StagnantShadowText]:
        image_path = [_.value for _ in StagnantShadow][[_.value for _ in StagnantShadowText].index(image_path)]

    ctrl.find_and_click(GUIDE, True, thresold=0.75)
    ctrl.find_and_click(SURVIVAL, try_times_limit=3)
    ctrl.find_and_click(STAGNANT_SHADOW)
    
    found = [False]
    while True:
        ctrl.find_and_click("stagnant/" + image_path, xOffset=500, try_times_limit=2, thresold=0.9, found=found, try_time_gap=0.33)
        if found[0] : break
        ctrl.dragRelPic(CREDIT, yOffset=-250)
        time.sleep(0.5)
    
    autobattle(times, hit=True, repByFuel=repByFuel)

# 侵蝕隧洞
def cavern_battle(image_path, times=1, repByFuel=False):
    global action_thread_stop
    if action_thread_stop[0] : return

    if image_path in [_.value for _ in CavernText]:
        image_path = [_.value for _ in Cavern][[_.value for _ in CavernText].index(image_path)]

    ctrl.find_and_click(GUIDE, True, thresold=0.75)
    ctrl.find_and_click(SURVIVAL, try_times_limit=3)

    found = [False]
    while True:
        ctrl.find_and_click(CAVERN_OF_CORROSION, try_times_limit=2, found=found, try_time_gap=0.33)
        if found[0] : break
        ctrl.dragRelPic(STAGNANT_SHADOW, yOffset=-250)
        time.sleep(0.5)

    found = [False]
    while True:
        ctrl.find_and_click("cavern/" + image_path, xOffset=500, try_times_limit=2, thresold=0.9, found=found, try_time_gap=0.33)
        if found[0] : break
        ctrl.dragRelPic(TRAILBLAZE_EXP, yOffset=-250)
        time.sleep(0.5)
    autobattle(times, hit=True, repByFuel=repByFuel)

# 歷戰餘響
def echo_battle(image_path, times=1, repByFuel=False):
    global action_thread_stop
    if action_thread_stop[0] : return

    if image_path in [_.value for _ in EchoText]:
        image_path = [_.value for _ in Echo][[_.value for _ in EchoText].index(image_path)]

    ctrl.find_and_click(GUIDE, True, thresold=0.75)
    ctrl.find_and_click(SURVIVAL, try_times_limit=3)

    found = [False]
    while True:
        ctrl.find_and_click(ECHO_OF_WAR, try_times_limit=2, found=found, try_time_gap=0.33)
        if found[0] : break
        ctrl.dragRelPic(STAGNANT_SHADOW, yOffset=-250)
        time.sleep(0.5)

    found = [False]
    while True:
        ctrl.find_and_click("echo/" + image_path, xOffset=500, try_times_limit=2, thresold=0.9, found=found, try_time_gap=0.33)
        if found[0] : break
        ctrl.dragRelPic(TRAILBLAZE_EXP, yOffset=-250)
        time.sleep(0.5)

    autobattle(times, hit=True, repByFuel=repByFuel)

# 領取委託
def assignment():
    global action_thread_stop
    if action_thread_stop[0] : return

    ctrl.find_and_click(PHONE, alt=True, thresold=0.85)
    ctrl.find_and_click(ASSIGNMENT)
    interrupt = [False]
    ctrl.find_and_click(FAST_CLAIM, try_times_limit=3, interrupt=interrupt)
    if not interrupt[0] : ctrl.find_and_click(ASSIGNMENT_AGAIN)
    ctrl.find_and_click(CLOSE)
    time.sleep(1.5)
    ctrl.find_and_click(CLOSE)

# 無名勳禮
def nameless_honor():
    global action_thread_stop
    if action_thread_stop[0] : return

    ctrl.find_and_click(NAMELESS_HONOR, alt=True, thresold=0.75)
    ctrl.find_and_click(MISSIONS)
    ctrl.find_and_click(FAST_CLAIM, try_times_limit=5)
    time.sleep(1.5)
    ctrl.find_and_click(REWARDS)
    interrupt = [False]
    time.sleep(1.5)
    ctrl.find_and_click(FAST_CLAIM, try_times_limit=5, interrupt=interrupt)
    if not interrupt[0] : ctrl.find_and_click(SPACE_CLOSE)
    ctrl.find_and_click(CLOSE)

# 啟動遊戲
def start_game():
    print("正在啟動遊戲...")
    ctrl.find_and_click("startgame.png")
    ctrl.find_and_click("enter.png")

# 離開遊戲
def exit_game():
    print("正在離開遊戲...")
    ctrl.find_and_click(PHONE, alt=True, thresold=0.85)
    ctrl.find_and_click(BACK_TO_LOGIN)
    ctrl.find_and_click(CONFIRM)
    ctrl.find_and_click(EXIT_GAME)
    ctrl.find_and_click(CONFIRM_YELLOW)