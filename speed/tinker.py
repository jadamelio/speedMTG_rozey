from tkinter import *
import time
import win32gui
import win32api

from win32api import GetSystemMetrics
# WIDTH = 500
# HEIGHT = 500

WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
LINEWIDTH = 1
TRANSCOLOUR = 'gray'
title = 'Virtual whiteboard'
global old
old = ()
global HWND_t
HWND_t = 0

tk = Tk()
# tk.title(title)
tk.lift()
tk.wm_attributes("-topmost", True)
tk.wm_attributes("-transparentcolor", TRANSCOLOUR)
tk.attributes('-fullscreen', True)


state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128

canvas = Canvas(tk, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack()
canvas.config(cursor='tcross')
canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=TRANSCOLOUR, outline=TRANSCOLOUR)
canvas.create_text(WIDTH/2,HEIGHT/2,fill="white",font="Arial 20", text="TEXT GOES HERE")

def putOnTop(event):
    event.widget.unbind('<Visibility>')
    event.widget.update()
    event.widget.lift()
    event.widget.bind('<Visibility>', putOnTop)
def drawline(data):
    global old
    if old !=():
        canvas.create_line(old[0], old[1], data[0], data[1], width=LINEWIDTH)
    old = (data[0], data[1])

def enumHandler(hwnd, lParam):
    global HWND_t
    if win32gui.IsWindowVisible(hwnd):
        if title in win32gui.GetWindowText(hwnd):
            HWND_t = hwnd

win32gui.EnumWindows(enumHandler, None)

tk.bind('<Visibility>', putOnTop)
tk.focus()

running = 1
while running == 1:
    try:
        tk.update()
        time.sleep(0.01)
        if HWND_t != 0:
            windowborder = win32gui.GetWindowRect(HWND_t)
            cur_pos = win32api.GetCursorPos()
            state_left_new = win32api.GetKeyState(0x01)
            if state_left_new != state_left:
                if windowborder[0] < cur_pos[0] and windowborder[2] > cur_pos[0] and windowborder[1] < cur_pos[1] and windowborder[3] > cur_pos[1]:
                    drawline((cur_pos[0] - windowborder[0] - 5, cur_pos[1] - windowborder[1] - 30))
            else:
                old = ()
    except Exception as e:
        running = 0
        print("error %r" % (e))