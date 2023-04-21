import json
import math
import time
import tkinter as tk
import win32gui
from PIL import Image, ImageTk, ImageFilter
from pynput import mouse, keyboard
from pynput.keyboard import Key

#Create an instance of tkinter window or frame
root = tk.Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

#Make the window jump above all
root.geometry(f"{w}x{h}+0+0")
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")
root.attributes("-alpha", 0.75)
#hide decoraction
root.overrideredirect(True)

photo = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
img = ImageTk.PhotoImage(photo)
with open('gun.json') as f:
    guns = json.load(f)

canvas = tk.Canvas(root, width=w, height=h, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, image=img, anchor="nw")

root.config(bg='white')
canvas.config(bg='white')
gun = "flatline"
pos = []
hwnd = win32gui.GetForegroundWindow()

with open(guns[gun]['location'], "r") as f:
    i = 0
    prev = []
    for line in f:
        x, y = line.strip().split()
        if i > 0:
            vx = int(x) - prev[0]
            vy = int(y) - prev[1]
            angle = math.atan2(vx, vy) * 180 / math.pi
            pos.append(angle)
        prev = [int(x), int(y)]
        i += 1

gun_dict = {
    Key.f1: "flatline", 
    Key.f2: "r301", 
    Key.f3: "nemesis", 
    Key.f4: "r99", 
    Key.f5: "car", 
    Key.f6: "volt", 
    Key.f7: "re45"
}

def press(key):
    global gun, mode
    # try:
    if key == Key.f12:
        root.destroy()
    elif key == Key.f11:
        gun = None
    elif key in gun_dict:
        mode = 0 
        gun = gun_dict[key]
        pos.clear()

        with open(guns[gun]['location'], "r") as f:
            i = 0
            prev = []
            for line in f:
                x, y = line.strip().split()
                if i > 0:
                    vx = int(x) - prev[0]
                    vy = int(y) - prev[1]
                    angle = math.atan2(vx, vy) * 180 / math.pi
                    pos.append(angle)
                prev = [int(x), int(y)]
                i += 1

def click(x, y, button, pressed):
    global left, right
    if button == mouse.Button.left:
        left = pressed
    elif button == mouse.Button.right:
        right = pressed

def angle_correct(a):
    a = min(a,abs(360 - a))
    return a

def setAxisAngle(src, angle, dis, ratio):
    global img
    p = Image.open(src)
    p = p.rotate(angle)
    p = p.filter(ImageFilter.SMOOTH)
    p = p.resize((75, 75), resample=Image.Resampling.NEAREST)
    p = p.resize((75, 75), Image.ANTIALIAS)
    if dis != -1:
        if ratio >= 0.5:
            r = 255
            g = int(2 * (1-ratio) * 255)
        else:
            g = 255
            r = int(2 * ratio * 255)

        color = Image.new("RGBA",p.size,(r, g, 0, 255))
        result = Image.new("RGBA", (75, 75), (0, 0, 0, 0))
        mask = p.convert('L').resize(p.size)
        result.paste(color, (0, 0), mask)
        p = result
    
    photo.paste(p, (113 - round(math.sin(angle / 180*math.pi)*dis), 113 - round(math.cos(angle/180*math.pi)*dis)), p)
    img = ImageTk.PhotoImage(photo)
    canvas.create_image((w - img.width()) // 2, (h - img.height()) // 2, image=img, anchor="nw")

left = False
right = False
listener = keyboard.Listener(on_press=press)
mouseClick = mouse.Listener(on_click=click)

i = 0
d = 5
mode = 0
preInterval = 0

def main():
    global i, photo, img, mode, preInterval
    
    start_time = time.perf_counter()
    photo = Image.new('RGBA', (300, 300), (0, 0, 0, 0))

    if len(pos) == 0:
        root.after(1, main)
        return

    if gun == None:
        img = ImageTk.PhotoImage(photo)
        canvas.create_image((w - img.width()) // 2, (h - img.height()) // 2, image=img, anchor="nw")
        root.after(1, main)
        return
    
    ind = 0
    if mode != 2:
        interval = 60 / guns[gun]['RPM'] * 1000
    else:
        interval = 60 / guns[gun]['RPM1'] * 1000
    
    if guns[gun]['size'] == 32 and mode == 0:
        preInterval = interval
    setAxisAngle("./UI/arrow.png", pos[0], -1, 0)

    if left and right:
        if mode != 1:
            ind = int(i // interval) + 1
        else:
            ind = int((i - preInterval*23)//interval) + 24
        if ind < guns[gun]['size'] - 1:
            for j in range(ind, min(len(pos), ind + 9)):
                if guns[gun]['size'] == 32 and j > 23 and mode != 2:
                    interval = 60 / guns[gun]['RPM1'] * 1000
                    mode = 1
                    dis = (24 * preInterval + interval * (j - 23) - i) / d #because interval are less but passedtime need same.
                else:
                    dis = (j * interval - i) / d
                ratio = j / (guns[gun]['size'] - 1)
                setAxisAngle("./UI/next.png", pos[j], dis, ratio)
            i += (time.perf_counter() - start_time) * 1000 + 1
        elif guns[gun]['size'] == 32: #if gun is nemesis and charged full then switch mod to 1.
            mode = 2
    else:
        setAxisAngle("./UI/next.png", pos[0], 0, 0)
        i = 0
    
    root.after(1, main) #1 millisecond

    
listener.start()
mouseClick.start()

main()
root.mainloop()