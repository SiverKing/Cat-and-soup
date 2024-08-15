print("此程序由SiverKing制作，发行版exe程序文件原作者19.9元一份带教程包调试，如有二次售卖请到 siver.top 联系原作者，本项目为开源项目，能熟练使用python的同学可以不付费前往 github.com/SiverKing 获取使用\n\n使用前请确保看过教程视频\n请耐心等待程序启动，在还未让您拖动窗口时，请不要拖动窗口避免出错")


import pyautogui
import cv2
import numpy as np
import time
import tkinter as tk
from PIL import ImageGrab, ImageTk
import keyboard
import threading

from win32.lib import win32con
from win32 import win32api, win32gui, win32print
###获取缩放后的分辨率
def get_screen_size():
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    return {"width": width, "height": height}
width = get_screen_size()["width"]
height = get_screen_size()["height"]
print("缩放后的屏幕分辨率：",width, 'x', height)
if width != 1920 or height != 1080:
    while True:
        print("\n您的分辨率不是1920x1080!!! 请更改为1920x1080后再启动!!!\n您的分辨率不是1920x1080!!! 请更改为1920x1080后再启动!!!\n您的分辨率不是1920x1080!!! 请更改为1920x1080后再启动!!!")
        time.sleep(10)
# 单击
def click(x, y):
    # xx = round(width * (x/1920))
    # yy = round(height * (y/1080))
    # print(xx,", ",yy)
    pyautogui.click(x, y)
# 捕捉屏幕区域的函数
def capture_region(region):
    x, y, w, h = region
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

# 在捕获的区域中查找模板图像的函数
def find_template_in_region(region, template_path, name, threshold=0.58):
    screenshot = capture_region(region)
    template = cv2.imread(template_path, 0)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    # 获取最大匹配值
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 打印当前匹配相似度
    print(name+f"当前匹配相似度: {max_val:.2f}")
    # threshold = 0.58
    
    loc = np.where(res >= threshold)
    
    if len(loc[0]) > 0:
        return True
    return False

# 执行点击操作的函数
def perform_click_actions(click_points):
    # print('蜗牛匹配成功')
    for point in click_points:
        click(point[0], point[1])
        time.sleep(1)  # 在点击之间添加延迟
    # time.sleep(34)
    # click(782, 79) # 关闭广告

# 使用tkinter来框选区域
class RegionSelector:
    def __init__(self, root, screenshot):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.screenshot = ImageTk.PhotoImage(screenshot)
        self.canvas.create_image(0, 0, image=self.screenshot, anchor=tk.NW)
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.region = None
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        self.region = (min(self.start_x, end_x), min(self.start_y, end_y), abs(end_x - self.start_x), abs(end_y - self.start_y))
        self.root.quit()

def select_monitor_region():
    root = tk.Tk()
    screenshot = ImageGrab.grab()
    selector = RegionSelector(root, screenshot)
    root.mainloop()
    root.destroy()
    return selector.region
def lian_dian():
    print("(程序可以通过空格进行暂停，请不要跟程序抢鼠标,若按下空格后请等待出现“暂停中...”)\n正在自动收菜，升级设施，升级食谱...")
    i = 10
    while i != 0:
        i = i-1
        click(242, 991) # 收菜
        # time.sleep(0.05)
    i = 15
    while i != 0:
        i = i-1
        click(251, 884) # 升级
        # time.sleep(0.05)
    time.sleep(0.5)
    click(641, 901) # 进食谱
    time.sleep(1)
    click(641, 901) # 二次进食谱
    time.sleep(0.5)
    i = 15
    while i != 0:
        i = i-1
        click(614, 862) # 食谱升级
        # time.sleep(0.05)
    time.sleep(0.5)
    click(242, 991)
    time.sleep(1)
def stop_sta(stop=0):
    global flag
    if stop==0: # 状态查询
        if flag == 1: return True
        elif flag == 0: return False
    elif stop==1: # 暂停
        if flag == 0: flag = 1
        elif flag == 1: flag = 0
    elif stop==2: # 初始化
        flag = 0
def YiDong_sta(cmd=0):
    global y_flag
    if cmd==0: # 状态查询
        if y_flag == 1: return True
        elif y_flag == 0: return False
    elif cmd==1: # 暂停
        if y_flag == 0: y_flag = 1
        elif y_flag == 1: y_flag = 0
    elif cmd==2: # 初始化
        y_flag = 0
def key_task():
    while True:
        if keyboard.is_pressed('space'):
            time.sleep(0.2)
            stop_sta(1) # 修改暂停状态
            if stop_sta(): print('\n空格键被按下, 请等待出现 暂停中... 字样后操作')
            else: print('\n自动化启动')
        if keyboard.is_pressed('enter'):
            time.sleep(0.2)
            YiDong_sta(1)
        time.sleep(0.1)
# 主函数
def main():
    task_ok = 0
    stop_sta(2) # 初始化暂停状态
    YiDong_sta(2)
    thread = threading.Thread(target=key_task) # 创建线程
    thread.start() # 启动线程
    time.sleep(2)
    print("\n请将此窗口移动至右边，使其不在猫猫上面且不会被其他窗口挡住的地方，确定移动好后按键盘 回车键(Enter) 继续")

    while True:
        if YiDong_sta(): break
    err = 0
    
    # 使用鼠标框选监测区域
    print("\n请框选猫猫整个页面")
    region = select_monitor_region()
    # print("\n请框选猫猫右上角一小部分，大小可参照教程视频")
    # x_region = select_monitor_region()
    
    # 模板图像的路径
    template_path = ".\\img\\wn.png"
    qw_path = ".\\img\\qw.png"
    hd_path = ".\\img\\hd.png"
    gz_path = ".\\img\\gz.png"
    xj_path = ".\\img\\xj.png"
    shi_path = ".\\img\\shi.png"
    lw_path = ".\\img\\lw.png"
    jl_path = ".\\img\\jl.png"
    x_path = ".\\img\\x.png"
    xx_path = ".\\img\\xx.png"
    # 定义要点击的点 (x, y) (518, 107), 
    click_points = [(518, 107), (248, 986), (241, 272), (480, 533), (423, 597), (551, 592)]  # 示例值
    qw_points = [(518, 107), (248, 986), (241, 272), (480, 533), (423, 597), (551, 592)]  # 青蛙
    hd_points = [(518, 107), (248, 986), (241, 272), (480, 533), (423, 597)]  # 蝴蝶
    gz_points = [(518, 107), (248, 986), (511, 924), (434, 691), (551, 592)]  # 罐子
    xj_points = [(518, 107), (248, 986), (717, 674), (480, 839), (480, 839), (518, 107)]  # 
    lw_points = [(518, 107), (480, 623), (518, 107)]
    jl_points = [(562, 585)]
    x_points = [(723, 72)]  # xxx
    i=0
    while True:
        if stop_sta():
            if i==0: print("\n暂停中...(按空格可继续)\n暂停中...(按空格可继续)\n暂停中...(按空格可继续)")
            i=1
            time.sleep(1)
        else:
            i=0
            if find_template_in_region(region, x_path, '关闭广告', 0.75) or find_template_in_region(region, xx_path, '关闭广告', 0.75):
                print('关闭广告匹配成功！！！')
                time.sleep(3)
                perform_click_actions(x_points)
                time.sleep(1)
                if find_template_in_region(region, x_path, '关闭广告', 0.75) or find_template_in_region(region, xx_path, '关闭广告', 0.75):
                    print('触发二次关闭！！')
                    click(723, 72) # 触发二次关闭
                    time.sleep(1)
                # click(518, 107)
            lian_dian() # 自动收菜，升级设施，升级食谱
            if find_template_in_region(region, template_path, '蜗牛', 0.55):
                print('蜗牛匹配成功')
                perform_click_actions(click_points)
                time.sleep(37)
                
            elif find_template_in_region(region, qw_path, '青蛙'):
                print('青蛙匹配成功')
                perform_click_actions(qw_points)
                time.sleep(37)
                
            elif find_template_in_region(region, hd_path, '蝴蝶'):
                print('蝴蝶匹配成功')
                perform_click_actions(hd_points)
                time.sleep(1)
                if find_template_in_region(region, shi_path, '蝴蝶纠错'):
                    click(551, 592) # 点 是
                    time.sleep(1)
                time.sleep(37)

            elif find_template_in_region(region, gz_path, '罐子'):
                print('罐子匹配成功')
                perform_click_actions(gz_points)
                time.sleep(37)

            elif find_template_in_region(region, xj_path, '相机', 0.8):
                print('相机匹配成功')
                perform_click_actions(xj_points)
                time.sleep(1)

            err = err + 1
            print(err)
            if err >= 20:
                if find_template_in_region(region, lw_path, '礼物纠错'):
                    print('礼物纠错匹配成功')
                    perform_click_actions(lw_points)
                err = 0
            time.sleep(1)  # 添加延迟以避免高CPU使用率

if True:
    try:
        main()
    
        thread.join()
        print("程序结束")
    
    except:
        print("\n程序出错！请重启程序！\n程序出错！请重启程序！\n程序出错！请重启程序！")
    
