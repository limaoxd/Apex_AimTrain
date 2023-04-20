from cmath import sqrt
import json
import math
import time
import tkinter as tk
from multiprocessing.connection import Listener
from tracemalloc import start
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageDraw
from pynput import mouse, keyboard

#Create an instance of tkinter window or frame
root = tk.Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

#Make the window jump above all
root.geometry('%dx%d+%d+%d' % (w, h, 0, 0))
root.attributes('-topmost',True)
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
gun = guns['flatline']
pos = []
mouse_motion = [0, 0]

with open(gun['location'], "r") as f:
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

def press(key):
    global guns, gun, pos
    try:
        if key == key.f12:
            root.destroy()
        elif key == key.f1 or key == key.f2 or key == key.f3 or key == key.f4 or key == key.f5 or key == key.f6:
            if key == key.f1:
                gun = guns['flatline']
                print("change to flatline")
            elif key == key.f2:
                gun = guns['r301']
                print("change to r301")
            elif key == key.f3:
                gun = guns['r99']
                print("change to r99")
            elif key == key.f4:
                gun = guns['car']
                print("change to car")
            elif key == key.f5:
                gun = guns['volt']
                print("change to volt")
            elif key == key.f6:
                gun = guns['re45']
                print("change to re45")
            pos.clear()
            with open(gun['location'], "r") as f:
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
    except:
        #do nothing
        pass
         
def click(x, y, button, pressed):
    global left, right, mouse_motion
    if button == mouse.Button.left:
        left = pressed
    elif button == mouse.Button.right:
        right = pressed

def angle_correct(a):
    a = min(a,abs(360 - a))
    return a

def setAxisAngle(src, angle, dis, ratio):
    global canvas, img, photo, w, h
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
    
    photo.paste(p, (113 - round(math.sin(angle/180*math.pi)*dis), 113 - round(math.cos(angle/180*math.pi)*dis)), p)
    img = ImageTk.PhotoImage(photo)
    canvas.create_image((w - img.width()) // 2, (h - img.height()) // 2, image=img, anchor="nw")

left = False
right = False
listener = keyboard.Listener(on_press=press)
mouseClick = mouse.Listener(on_click=click)
timer = 0
i=0
d=5
def main():
    start_time = time.perf_counter()
    global canvas, left, right, gun, i, pos, timer, mouse_motion, root, photo, w, h
    photo = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
    ind = 0
    interval = 60 / gun['RPM'] * 1000
    maxdis = (gun['size'] - 1) * interval / d
    setAxisAngle("./UI/arrow.png", pos[0], -1, 0)
    if left and right:
        ind = int(i // interval) + 1
        if ind < gun['size'] - 1:
            for j in range(ind, min(len(pos), ind + 9)):    
                dis = (j * interval - i)/ d
                ratio = j / (gun['size'] - 1)
                setAxisAngle("./UI/next.png", pos[j], dis, ratio)
            i += (time.perf_counter() - start_time) * 1000 + 1
    else:
        setAxisAngle("./UI/next.png", pos[0], 0, 0)
        i = 0
    
    root.after(1, main) #1 millisecond
    
listener.start()
mouseClick.start()

main()
root.mainloop()