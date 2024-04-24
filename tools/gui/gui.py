from tools.dict import *
from tools import guide
import tkinter as tk
import tkinter.ttk as ttk
import threading
import json
import os

# region 全域變數

DATAPATH = './data.txt'

root = None

# buttons
start_button = None
insert_button = None

# comboboxs
action_box = None
place_box = None
target_box = None

# entrys
again_entry = None

# labels
again_label = None
notice_label = None

# listbox
action_listbox = None

# list_control_buttons
move_up_button = None
move_down_button = None
remove_button = None
all_start_button = None
interrupt_button = None

# plans
plan_canvas = None
newplan_button = None
plan_list = []
content_plan = None

# endregion

# 行動類(用於創建行動隊列)
class Action:
    def __init__(self, name, times=None, target=None, place=None):
        self.name = name
        try:
            self.times = int(times)
        except:
            self.times = times
        self.target = target
        self.place = place

    def start(self):
        if self.name == ASSIGNMENT_TEXT : guide.assignment()
        elif self.name == DAILY_REWARD_TEXT : guide.claim_daily_reward()
        elif self.name == NAMELESS_HONOR_TEXT : guide.nameless_honor()
        elif self.name == GOLDEN_FLOWER_TEXT : guide.flower_battle(color=self.name, times=self.times, target=self.target, place=self.place)
        elif self.name == CRIMSON_FLOWER_TEXT : guide.flower_battle(color=self.name, times=self.times, target=self.target, place=self.place)
        elif self.name == CAVERN_OF_CORROSION_TEXT : guide.cavern_battle(image_path=self.target, times=self.times)
        elif self.name == ECHO_OF_WAR_TEXT : guide.echo_battle(image_path=self.target, times=self.times)
        elif self.name == STAGNANT_SHADOW_TEXT : guide.stagnant_shadow_battle(image_path=self.target, times=self.times)

    def from_json(obj):
        return Action(obj['name'], obj['times'], obj['target'], obj['place'])

# 方案類(用於儲存不同行動隊列)
class Plan:
    def __init__(self, canvas=None, y=0, name=''):
        self.action_list = []
        self.canvas = canvas
        self.name = name.replace(' ', '_')
        self.y = y
        self.editing = False
        self.draw()
    
    def draw(self):
        self.frame = tk.Frame(self.canvas, width=185, height=75, bg='gray')
        self.id = self.canvas.create_window((0, self.y), window=self.frame, anchor=tk.NW)

        self.label_text = tk.StringVar()
        if self.name != None : self.label_text.set(self.name)
        else : self.label_text.set('default')
        self.label = tk.Label(self.frame, textvariable=self.label_text, font=('Arial', 11), bg='gray')
        self.label.place(x=5, y=5)

        self.edit_button = tk.Button(self.frame, text='編輯', height=1, font=('Arial', 11), command=lambda: self.edit())
        self.edit_button.place(x=7, y=40, width=50)

        self.done_button = tk.Button(self.frame, text='確認', height=1, font=('Arial', 11), command=lambda: self.edit_done())

        self.delete_button = tk.Button(self.frame, text='刪除', height=1, font=('Arial', 11), command=lambda: self.delete())
        self.delete_button.place(x=127, y=40, width=50)

        self.load_button = tk.Button(self.frame, text="載入", height=1, font=('Arial', 11), command=lambda: self.load())
        self.load_button.place(x=67, y=40, width=50)

        self.entry = tk.Entry(self.frame)
        self.entry.bind("<Return>", lambda event: self.edit_done())

    def set_disabled(self):
        self.edit_button.config(state=tk.DISABLED)
        self.done_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.load_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)

    def set_enabled(self):
        self.edit_button.config(state=tk.NORMAL)
        self.done_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)
        self.load_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)

    def edit(self):
        self.edit_button.place_forget()
        self.done_button.place(x=7, y=40, width=50)
        self.editing = True

        self.entry.place(x=5, y=7, width=120)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.name)
        self.entry.select_range(0, tk.END)
        self.entry.focus_set()

    def edit_done(self):
        if not self.editing : return 
        self.editing = False

        self.name = self.entry.get().replace(' ', '_')
        self.label_text.set(self.name)
        self.entry.place_forget()
        self.done_button.place_forget()
        self.edit_button.place(x=7, y=40, width=50)
        plan_save()

    def load(self):
        global content_plan
        content_plan = self
        Log.print(f'已設為方案 {self.name}')
        draw_action_listbox()
        draw_plan_canvas()

    def remove_from_canvas(self):
        self.canvas.delete(self.id)

    def redraw_on_canvas(self, y):
        self.id = self.canvas.create_window((0, y), window=self.frame, anchor=tk.NW)
        if content_plan == self : self.label.config(font=('Arial', 11, 'bold'), fg='white')
        else : self.label.config(font=('Arial', 11), fg='black')

    def delete(self):
        global plan_list, content_plan
        self.canvas.delete(self.id)
        plan_list.remove(self)
        self.frame.destroy()

        if len(plan_list) != 0 : 
            content_plan = plan_list[0]
            Log.print(f'已設為方案 {content_plan.name}')
        else : content_plan = None

        draw_plan_canvas()
        draw_action_listbox()
        plan_save()

        del self

# 日誌類
class Log:
    _instance = None
    root = None
    textbox = None

    @classmethod
    def get_instance(cls, root=None, x=0, y=0, height=0, width=0):
        if cls._instance is None and root != None:
            cls._instance = cls(root, x, y, height, width)
        return cls._instance
    
    def __init__(self, root, x, y, height, width):
        self.root = root
        self.textbox = tk.Text(root)
        self.textbox.place(x=x, y=y, height=height, width=width)

    @staticmethod
    def print(value):
        Log.get_instance().textbox.config(state=tk.NORMAL)
        Log.get_instance().textbox.insert(tk.END, value + '\n')
        Log.get_instance().textbox.see(tk.END)
        Log.get_instance().textbox.config(state=tk.DISABLED)

# region 繪製GUI函數

# 移除閒置物件
def forget_object(object):
    if object != None :
        object.place_forget()
        if hasattr(object, "set"):
            object.set(0)
        elif hasattr(object, "delete"):
            object.delete(0, tk.END)

# 整數輸入認證
def validate_input(new_value):
    if new_value.isdigit() or new_value == "" : return True
    else : return False

# 繪製行動選項
def draw_action_options(value=None):
    global root, place_box, target_box, again_label, again_entry, notice_label, start_button, insert_button, action_box
    forget_object(place_box); forget_object(target_box); forget_object(again_label); forget_object(again_entry); forget_object(notice_label); forget_object(start_button); forget_object(insert_button)
    
    if value == GOLDEN_FLOWER_TEXT :

        places = [text.value for text in PlaceText]
        place_box = ttk.Combobox(root, values=places, state="readonly")
        place_box.current(0)
        place_box.place(x=210, y=65)

        targets = [CHARACTER_EXP_TEXT, CREDIT_TEXT, LIGHT_CONE_EXP_TEXT]
        target_box = ttk.Combobox(root, values=targets, state="readonly")
        target_box.current(0)
        target_box.place(x=210, y=95)
        

        again_label = tk.Label(root, text="要進行幾次?", height=1, font=('Arial', 12))
        again_label.place(x=210, y=125)
        again_input = root.register(validate_input)

        again_entry = tk.Entry(root, validate="key", validatecommand=(again_input, '%P'))
        again_entry.place(x=310, y=127, width=65)
        again_entry.insert(0, "1")

        notice_label = tk.Label(root, text="花萼類會進入6回合的挑戰!!", height=1, font=('Arial', 10))
        notice_label.place(x=210, y=155)

        # start_button = tk.Button(root, text="直接開始", height=1, font=('Arial', 11), command=action_start)
        # start_button.place(x=210, y=185)

        insert_button = tk.Button(root, text="插入隊列", height=1, font=('Arial', 11), command=action_insert)
        insert_button.place(x=210, y=185, width=167)
        
    elif value == ECHO_OF_WAR_TEXT or value == STAGNANT_SHADOW_TEXT or value == CAVERN_OF_CORROSION_TEXT or value == CRIMSON_FLOWER_TEXT :

        if value == ECHO_OF_WAR_TEXT : targets = [text.value for text in EchoText]
        elif value == STAGNANT_SHADOW_TEXT : targets = [text.value for text in StagnantShadowText]
        elif value == CAVERN_OF_CORROSION_TEXT : targets = [text.value for text in CavernText]
        elif value == CRIMSON_FLOWER_TEXT : targets = [text.value for text in CrimsonFlowerText]
        target_box = ttk.Combobox(root, values=targets, state="readonly")
        target_box.current(0)
        target_box.place(x=210, y=65)

        again_label = tk.Label(root, text="要進行幾次?", height=1, font=('Arial', 12))
        again_label.place(x=210, y=95)
        again_input = root.register(validate_input)

        again_entry = tk.Entry(root, validate="key", validatecommand=(again_input, '%P'))
        again_entry.place(x=310, y=97, width=65)
        again_entry.insert(0, "1")

        if value == CRIMSON_FLOWER_TEXT:
            notice_label = tk.Label(root, text="花萼類會進入6回合的挑戰!!", height=1, font=('Arial', 10))
            notice_label.place(x=210, y=155)

        # start_button = tk.Button(root, text="直接開始", height=1, font=('Arial', 11), command=action_start)
        # start_button.place(x=210, y=185)

        insert_button = tk.Button(root, text="插入隊列", height=1, font=('Arial', 11), command=action_insert)
        insert_button.place(x=210, y=185, width=167)

    elif value == NAMELESS_HONOR_TEXT or value == DAILY_REWARD_TEXT or value == ASSIGNMENT_TEXT :

        # start_button = tk.Button(root, text="直接開始", height=1, font=('Arial', 11), command=action_start)
        # start_button.place(x=210, y=185)

        insert_button = tk.Button(root, text="插入隊列", height=1, font=('Arial', 11), command=action_insert)
        insert_button.place(x=210, y=185, width=167)

    elif value == None:
        
        action_box.current(0)

# 繪製方案畫布
def draw_plan_canvas():
    global plan_list, plan_canvas, newplan_button

    plan_canvas.delete('all')

    nowy = 0

    for plan in plan_list:
        plan.redraw_on_canvas(nowy)
        nowy += 80

    newplan_button = tk.Button(plan_canvas, text='新增方案', height=1, font=('Arial', 11), command=new_plan)
    plan_canvas.create_window((17, nowy+5), width=150, window=newplan_button, anchor=tk.NW)

    plan_canvas.configure(scrollregion=plan_canvas.bbox('all'))

# 繪製行動隊列
def draw_action_listbox():
    global content_plan, action_listbox
    action_listbox.delete(0, tk.END)

    if content_plan == None : return

    for action in content_plan.action_list:
        if action.name in [NAMELESS_HONOR_TEXT, DAILY_REWARD_TEXT, ASSIGNMENT_TEXT] :
            action_listbox.insert(tk.END, f'{action.name}')
        elif action.name == GOLDEN_FLOWER_TEXT:
            action_listbox.insert(tk.END, f'{action.name} {action.place} {action.target} {action.times} 次')
        else:
            action_listbox.insert(tk.END, f'{action.name} {action.target} {action.times} 次')

# endregion

# region action 相關

# 行動選擇
def on_action_selected(event:tk.Event):
    global action_box
    if action_box == None : return
    draw_action_options(action_box.get())

# 插入行動
def action_insert():
    global action_box, again_entry, target_box, place_box, notice_label, action_listbox, content_plan

    if content_plan == None: new_plan()

    name = action_box.get()
    if name == ASSIGNMENT_TEXT or name == DAILY_REWARD_TEXT or name == NAMELESS_HONOR_TEXT:
        content_plan.action_list.append(Action(name=name))
        action_listbox.insert(tk.END, name) 
        Log.print(f'已在 {content_plan.name} 插入 {name}')
        plan_save()
        return

    try : again = int(again_entry.get())
    except : again = 0

    if again < 1:
        forget_object(notice_label)
        notice_label = tk.Label(root, text="請輸入大於等於1的整數!!", height=1, font=('Arial', 10))
        notice_label.place(x=10, y=155)
        return
    
    if name in [GOLDEN_FLOWER_TEXT]:
        content_plan.action_list.append(Action(name=name, times=again, target=target_box.get(), place=place_box.get()))
        action_listbox.insert(tk.END, f'{name} {place_box.get()} {target_box.get()} {again} 次')
    else:
        content_plan.action_list.append(Action(name=name, times=again, target=target_box.get()))
        action_listbox.insert(tk.END, f'{name} {target_box.get()} {again} 次')

    Log.print(f'已在 {content_plan.name} 插入 {name}')
    plan_save()

# 移除行動
def action_remove():
    global action_listbox, content_plan
    selected_index = action_listbox.curselection()
    if selected_index == () : return
    name = content_plan.action_list[selected_index[0]].name
    action_listbox.delete(selected_index)
    content_plan.action_list.pop(selected_index[0]) # selected_index 為元組 因此要選出第一個
    if action_listbox.size() != 0 : 
        if selected_index[0] < action_listbox.size() : action_listbox.select_set(selected_index[0])
        else : action_listbox.select_set(selected_index[0] - 1)
    Log.print(f'已從方案 {content_plan.name} 移除 {name}')
    plan_save()

# 上移行動
def action_moveup():
    global action_listbox, content_plan
    selected_index = action_listbox.curselection()
    if selected_index == () : return
    i = selected_index[0]
    if i <= 0 : return 
    tmp = action_listbox.get(i)
    atmp = content_plan.action_list[i]
    content_plan.action_list.pop(i)
    content_plan.action_list.insert(i-1, atmp)
    action_listbox.delete(i)
    action_listbox.insert(i-1, tmp)
    action_listbox.selection_set(i-1)
    plan_save()

# 下移行動
def action_movedown():
    global action_listbox, content_plan
    selected_index = action_listbox.curselection()
    if selected_index == () : return
    i = selected_index[0]
    if i >= action_listbox.size() - 1 : return
    tmp = action_listbox.get(i)
    atmp = content_plan.action_list[i]
    content_plan.action_list.pop(i)
    content_plan.action_list.insert(i+1, atmp)
    action_listbox.delete(i)
    action_listbox.insert(i+1, tmp)
    action_listbox.selection_set(i+1)
    plan_save()

# 行動隊列開始執行
def action_list_start():
    global content_plan
    if content_plan.action_list == []:
        Log.print('未加入任何行動')
        return
    Log.print('行動隊列執行中...')
    this_thread = threading.Thread(target=t_action_list_start)
    this_thread.start()

# 多線程
def t_action_list_start():

    all_start_button.place_forget()
    interrupt_button.place(x=480, y=355, width=200)
    all_set_disabled()

    action_thread_stop[0] = False
    for i in content_plan.action_list:
        if action_thread_stop[0] :
            break
        Log.print(f'正在執行 {i.name}')
        task_thread = threading.Thread(target=i.start)
        task_thread.start()
        task_thread.join()

    all_set_enabled()
    interrupt_button.place_forget()
    all_start_button.place(x=480, y=355, width=200)

    Log.print('行動隊列執行完畢!')

# 中斷隊列
def interrupt_action_list():
    global action_thread_stop
    action_thread_stop[0] = True
    Log.print('正在中斷行動列隊執行... *此操作可能需等待3-5秒')

# endregion

# region plan 相關

# 所有方案保存
def plan_save():
    global plan_list
    with open(DATAPATH, 'w') as file:
        for plan in plan_list:
            file.write(plan.name + ' ' + str(len(plan.action_list)) + '\n')
            actions = [json.dumps(action.__dict__) for action in plan.action_list]

            ret = ''
            for action in actions:
                ret += action + '\n'

            file.write(ret)

# 所有方案讀取
def plan_load():
    global plan_list, plan_canvas, content_plan
    Log.print('載入方案中...')
    if not os.path.exists(DATAPATH):
        Log.print(f'未檢測到 {DATAPATH}!, 已創建新存檔')
        new_plan()
        return
    
    with open(DATAPATH, 'r') as file:
        check = False
        content_plan = None
        count = 0
        action_nums = 0
        for line in file:
            line = line.strip()
            if check == False:
                content_plan = Plan(canvas=plan_canvas, name=line.split(' ')[0])
                plan_list.append(content_plan)

                check = True
                action_nums = int(line.split(' ')[1])
                count = 0
            else:
                action = json.loads(line, object_hook=Action.from_json)
                content_plan.action_list.append(action)
                count += 1

            if count == action_nums : check = False
        Log.print('方案載入成功!')
        draw_plan_canvas()
        if len(plan_list) == 0 : return
        content_plan = plan_list[0]
        draw_action_listbox()
        Log.print(f'已設為方案 {content_plan.name}')

# 新增方案
def new_plan():
    global plan_list, plan_canvas, content_plan
    plan = Plan(canvas=plan_canvas, name='New_Plan')
    content_plan = plan
    plan_list.append(plan)
    draw_plan_canvas()
    draw_action_listbox()
    Log.print(f'已設為方案 {content_plan.name}')
    plan_save()

# endregion

# region 其他函數

# 取消所有物件交互
def all_set_disabled():
    global plan_list, newplan_button, move_up_button, move_down_button, remove_button, action_box
    for plan in plan_list:
        plan.set_disabled()
    draw_action_options()
    action_box.config(state=tk.DISABLED)
    newplan_button.config(state=tk.DISABLED)
    move_down_button.config(state=tk.DISABLED)
    move_up_button.config(state=tk.DISABLED)
    remove_button.config(state=tk.DISABLED)

# 恢復所有物件交互
def all_set_enabled():
    global plan_list, newplan_button, move_up_button, move_down_button, remove_button, action_box
    for plan in plan_list:
        plan.set_enabled()
    action_box.config(state=tk.NORMAL)
    newplan_button.config(state=tk.NORMAL)
    move_down_button.config(state=tk.NORMAL)
    move_up_button.config(state=tk.NORMAL)
    remove_button.config(state=tk.NORMAL)
    
# 凝滯虛影戰鬥
def stagnant_shadow_battle():
    global action_box, again_entry, target_box, place_box, notice_label
    guide.stagnant_shadow_battle(image_path=target_box(), times=int(again_entry.get()), repByFuel=False)

# 侵蝕隧洞戰鬥
def cavern_battle():
    global action_box, again_entry, target_box, place_box, notice_label
    guide.cavern_battle(image_path=target_box.get(), times=int(again_entry.get()), repByFuel=False)

# 歷戰餘響戰鬥
def echo_battle():
    global action_box, again_entry, target_box, place_box, notice_label
    guide.echo_battle(image_path=target_box.get(), times=int(again_entry.get()), repByFuel=False)

# 擬造花萼(赤)戰鬥
def crimson_flower_battle():
    global action_box, again_entry, target_box, place_box, notice_label
    guide.flower_battle(action_box.get(), times=int(again_entry.get()), target=target_box.get())

# 擬造花萼(金)戰鬥
def golden_flower_battle():
    global action_box, again_entry, target_box, place_box, notice_label
    guide.flower_battle(action_box.get(), times=int(again_entry.get()), target=target_box.get(), place=place_box.get())

# endregion

# region 棄用函數 此區塊函數不會更新迭代 使用時需檢查函數內部的變數及用法是否已發生改變或棄用

# 方案畫布點擊 已棄用
def on_canvas_click(event):
    global plan_canvas
    plan_canvas.scan_mark(event.x, event.y)

# 方案畫布拖動 已棄用
def on_canvas_drag(event):
    global plan_canvas
    plan_canvas.scan_dragto(plan_canvas.winfo_x(), event.y, gain=1)

# 開始執行單一行動 已棄用
def action_start():
    this_thread = threading.Thread(target=t_action_start)
    this_thread.start()

# 多線程執行單一行動 已棄用
def t_action_start():
    global action_box, again_entry, target_box, place_box, notice_label, start_button, interrupt_button

    start_button.place_forget()
    interrupt_button.place(x=210, y=185)
    all_set_disabled()

    Log.print(f'正在執行 {action_box.get()}')

    if action_box.get() == ASSIGNMENT_TEXT : guide.assignment()
    elif action_box.get() == DAILY_REWARD_TEXT : guide.claim_daily_reward()
    elif action_box.get() == NAMELESS_HONOR_TEXT : guide.nameless_honor()

    try : again = int(again_entry.get())
    except : again = 0

    if again < 1:
        forget_object(notice_label)
        notice_label = tk.Label(root, text="請輸入大於等於1的整數!!", height=1, font=('Arial', 10))
        notice_label.place(x=10, y=155)
        return

    if action_box.get() == GOLDEN_FLOWER_TEXT : golden_flower_battle()
    elif action_box.get() == CRIMSON_FLOWER_TEXT : crimson_flower_battle()
    elif action_box.get() == STAGNANT_SHADOW_TEXT : stagnant_shadow_battle()
    elif action_box.get() == CAVERN_OF_CORROSION_TEXT : cavern_battle()
    elif action_box.get() == ECHO_OF_WAR_TEXT : echo_battle()

    interrupt_button.place_forget()
    all_set_enabled()

# endregion

# 主函式
def main():
    global root, action_box, action_listbox, plan_canvas, plan_list, content_plan, move_up_button, move_down_button, remove_button, all_start_button, interrupt_button, Log_print
    root = tk.Tk()

    # 主視窗
    root.title("AutoRail_0.1")
    root.geometry("700x600")
    root.resizable(False, False)

    # region 方案選單

    # 畫布
    plan_canvas = tk.Canvas(root, width=195, height=590, bg='lightblue')
    plan_canvas.place(x=5, y=5)
    # plan_canvas.bind("<ButtonPress-1>", on_canvas_click)
    # plan_canvas.bind("<B1-Motion>", on_canvas_drag)

    canvas_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=plan_canvas.yview)
    canvas_scrollbar.place(x=190, y=5, height=595)
    plan_canvas.configure(yscrollcommand=canvas_scrollbar.set)

    # endregion

    # region 左側選擇欄位

    # 左側首行Label
    labelText = tk.StringVar(value="選擇要自動進行的事項")
    myLabel = tk.Label(root, textvariable=labelText, height=1, font=('Arial', 12))
    myLabel.place(x=210, y=5)
    
    # 選項框
    actions = ["(選擇要進行的事項)", STAGNANT_SHADOW_TEXT, GOLDEN_FLOWER_TEXT, CRIMSON_FLOWER_TEXT, CAVERN_OF_CORROSION_TEXT, ECHO_OF_WAR_TEXT, NAMELESS_HONOR_TEXT, ASSIGNMENT_TEXT, DAILY_REWARD_TEXT]
    action_box = ttk.Combobox(root, values=actions, state='readonly')
    action_box.current(0)
    action_box.bind("<<ComboboxSelected>>", on_action_selected)
    action_box.place(x=210, y=35)

    # endregion

    # region 右側隊列

    # 右側首行Label
    listLabelText = tk.StringVar(value="執行隊列")
    listLabel = tk.Label(root, textvariable=listLabelText, height=1, font=('Arial', 12))
    listLabel.place(x=480, y=5)

    # 行動隊列滾動條
    scollbar = tk.Scrollbar(root)
    scollbar.place(x=680, y=35, height=245)
    
    # 行動隊列顯示框
    action_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    action_listbox.place(x=480, y=35, width=200, height=245)
    action_listbox.config(yscrollcommand=scollbar.set)
    # 滾動條與顯示框連結
    scollbar.config(command=action_listbox.yview)

    # 行動隊列上移按鈕
    move_up_button = tk.Button(root, text="上移", height=1, font=('Arial', 11), command=action_moveup)
    move_up_button.place(x=480, y=285, width=95)

    # 下移按鈕
    move_down_button = tk.Button(root, text="下移", height=1, font=('Arial', 11), command=action_movedown)
    move_down_button.place(x=585, y=285, width=95)

    # 存檔按鈕
    # save_button = tk.Button(root, text="儲存", height=1, font=('Arial', 11), command=plan_save)
    # save_button.place(x=480, y=320, width=95)

    # 刪除單一行動按鈕
    remove_button = tk.Button(root, text="刪除", height=1, font=('Arial', 11), command=action_remove)
    remove_button.place(x=480, y=320, width=200)

    # 隊列開始按鈕
    all_start_button = tk.Button(root, text="開始執行隊列", height=1, font=('Arial', 11), command=action_list_start)
    all_start_button.place(x=480, y=355, width=200)

    # 中斷按鈕
    interrupt_button = tk.Button(root, text='中斷執行', height=1, font=('Arial', 11), command=interrupt_action_list)


    # endregion

    Log.get_instance(root=root, x=205, y=400, height=190, width=490)

    Log_print.append(Log.print)

    plan_load()

    root.mainloop()