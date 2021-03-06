import sys
#import pygame
import logging

from dia import *

try:
    # for Python2
    import Tkinter as tk   ## notice capitalized T in Tkinter
    import ttk
    import tkSimpleDialog as simpledialog
except ImportError:
    # for Python3
    import tkinter as tk   ## notice lowercase 't' in tkinter here
    from tkinter import ttk
    from tkinter import simpledialog, colorchooser, messagebox


app = tk.Tk()

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)
  
# Setting up color objects
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

NUM_OF_LEDS = 80

DIGITS_TO_DISPLAY = len(str(NUM_OF_LEDS))
pixelVirtual = tk.PhotoImage(width=1, height=1)

class LED(): ### will have the color property, index and the button associated with it. 
    def __init__(self, index, frame):
        self.index = index
        self.color = str(GRAY)
        self.bt = tk.Button(frame, bg='gray')

    def setcolor(self,color):
        self.color = color
        self.bt['bg'] = textohex(color)[1]

class LedBlock(): ### will have indices for the LEDs
    def __init__(self, parent, initial_led = 0, num_leds = NUM_OF_LEDS, name="Unnamed block"):
        self.frame = tk.Frame(parent, relief=tk.RIDGE, borderwidth=1)
        self.frame.pack(side=tk.TOP, anchor=tk.NW)
        self.namelabel = tk.Label(self.frame, width=25, text=name)
        self.namelabel.pack()
        self.led_button_array = []

        for i in range(initial_led, num_leds):
            self.led_button_array.append(LED(i,self.frame))

        for i, led in enumerate(self.led_button_array):
            led.bt['text'] = "" 
            led.bt['width'] = 10
            led.bt['height'] = 10
            led.bt['image'] = pixelVirtual
            led.bt['command'] = leddia(app, i, led)
            led.bt.pack(side="left")

class LedArray(): ### will have the LEDs objs as an array
    def __init__(self):
        pass

def show_vis(): ## at some point will show maybe 3d?
    pass

def main():
    #app = tk.Tk()

    app.geometry("1600x800")
    app.title("Brain LEDS")
    app.resizable(width=False,height=False)
    #app.withdraw()
    top_frame = tk.Frame(app, relief=tk.RIDGE, borderwidth=1)
    top_frame.pack(side = tk.TOP, fill= tk.X)
    top_frame_left_frame = tk.Frame(top_frame)
    top_frame_left_frame.pack(side=tk.LEFT) 
    canvas = tk.Canvas(top_frame_left_frame, width = 180, height = 180)
    canvas.pack()
    img = tk.PhotoImage(file="logo32x32.png")
    canvas.create_image(0,0,anchor=tk.NW, image = img)
    
    animation_frame = tk.Frame(top_frame, relief=tk.RIDGE, borderwidth=1)
    animation_frame.pack(side=tk.RIGHT)
    animation_canvas = tk.Canvas(animation_frame, width = NUM_OF_LEDS, height = 600, bg='#000000')    
    animation_canvas.pack(side=tk.RIGHT)
    pattern_img = tk.PhotoImage(file="pattern.png")
    animation_canvas.create_image(0,0, anchor=tk.NW, image = pattern_img)

    load_button = tk.Button(animation_frame, text = "load")
    load_button.pack(side=tk.TOP, fill=tk.X)
    save_button = tk.Button(animation_frame, text = "save")
    save_button.pack(side=tk.TOP, fill=tk.X)

    up_button = tk.Button(animation_frame, text = "up")
    up_button.pack(side=tk.TOP, fill=tk.X)

    down_button = tk.Button(animation_frame, text = "down")
    down_button.pack(side=tk.TOP, fill=tk.X)

    layer_frame = tk.Frame(animation_frame)
    layer_frame.pack(side=tk.TOP)

    layer_text = tk.Label(layer_frame, text= "Curr. Layer")
    layer_text.pack(side=tk.LEFT)

    layer_num = tk.Entry(layer_frame,text = "0")
    layer_num.pack(side=tk.RIGHT)

    allLeds = LedBlock(parent = top_frame_left_frame, name="All LEDs 0")
    #allLeds1 = LedBlock(parent = top_frame_left_frame, name="All LEDs 1")
    #allLeds2 = LedBlock(parent = top_frame_left_frame, name="All LEDs 2")

    app.protocol("WM_DELETE_WINDOW", on_closing)

    lower_frame = tk.Frame(app, relief=tk.RIDGE, borderwidth=1)
    lower_frame.pack(side=tk.BOTTOM)
    ok_button = tk.Button(lower_frame, text='Start', width=50, command=show_vis)
    ok_button.pack(side=tk.BOTTOM, anchor=tk.NW, fill="both")

    fps_frame = tk.Frame(lower_frame, relief=tk.RIDGE, borderwidth=1)
    fps_frame.pack(side=tk.TOP)

    fps_text = tk.Label(fps_frame, text= "FPS")
    fps_text.pack(side=tk.LEFT)

    fps_num = tk.Entry(fps_frame,text = "30")
    fps_num.pack(side=tk.RIGHT)

 

    
    # app.update()
    app.mainloop()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #try:
        app.destroy()            
        sys.exit()
        #except:
        #    pass

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    try:
        main()
    except KeyboardInterrupt:
        pass
