import json
import math
import time
import tkinter as tk
from multiprocessing.connection import Listener
from tracemalloc import start
from PIL import Image, ImageTk, ImageFilter
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

photo = Image.open("./UI/arrow.png")
with open('gun.json') as f:
    guns = json.load(f)

photo = photo.resize((75, 75), resample=Image.NEAREST)
img = ImageTk.PhotoImage(photo)
W = img.width()
H = img.height()

canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, image=img, anchor="nw")
canvas.place(x=(w-W)/2, y=(h-H)/2)

root.config(bg='white')
canvas.config(bg='white')
gun = guns['flatline']
pos = []

with open(gun['location'], "r") as f:
    for line in f:
        x, y = line.strip().split()
        pos.append([int(x), int(y)])

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
                for line in f:
                    x, y = line.strip().split()
                    pos.append([int(x), int(y)])
    except:
        #do nothing
        pass
         
def click(x, y, button, pressed):
    global left, right
    if button == mouse.Button.left:
        left = pressed
    elif button == mouse.Button.right:
        right = pressed

def setAxisAngle(angle):
    global canvas, photo, img
    canvas.rotate_angle = angle
    canvas.delete("all")
    photo = Image.open("./UI/arrow.png")
    photo = photo.rotate(angle)
    photo = photo.filter(ImageFilter.SMOOTH)
    photo = photo.resize((75, 75), resample=Image.Resampling.NEAREST)
    photo = photo.resize((75, 75), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(photo)
    canvas.create_image(0, 0, image=img, anchor="nw")

left = False
right = False
listener = keyboard.Listener(on_press=press)
mouseClick = mouse.Listener(on_click=click)
timer = 0
i=0

def main():
    start_time = time.perf_counter()
    global left, right, gun, i, pos, timer
    interval = 60 / gun['RPM'] * 1000
    if left and right:
        ind = int(i // interval) + 1
        if ind < gun['size'] - 2:
            vx = pos[int(ind + 1)][0] - pos[ind][0]
            vy = pos[int(ind + 1)][1] - pos[ind][1] #multiply - is mean screen x,y system's y is invert
            angle = math.atan2(vx, vy) * 180 / math.pi
            #print(str(vx) + " " + str(vy) + " " + str(angle))
            setAxisAngle(angle)
            i += (time.perf_counter() - start_time) * 1000
    else:
        vx = pos[1][0] - pos[0][0]
        vy = pos[1][1] - pos[0][1] #multiply - is mean screen x,y system's y is invert
        angle = math.atan2(vx, vy) * 180 / math.pi
        setAxisAngle(angle)
        i = 0
    root.after(1, main) #1 millisecond

listener.start()
mouseClick.start()
main()
root.mainloop()