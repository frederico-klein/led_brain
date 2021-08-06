import sys
import pygame
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

class LedArray():
    def __init__(self):
        pass

class LedBlock():
    def __init__(self):
        pass

class LED():
    def __init__(self):
        pass

def show_vis():
    pass

def main():
    #app = tk.Tk()

    app.geometry("1600x300")
    app.title("Brain LEDS")
    app.resizable(width=False,height=False)
    #app.withdraw()
    canvas = tk.Canvas(app, width = 180, height = 180)
    canvas.pack()
    img = tk.PhotoImage(file="logo32x32.png")
    canvas.create_image(0,0,anchor=tk.NW, image = img)
    pixelVirtual = tk.PhotoImage(width=1, height=1)

    led_button_array = []
    for i in range(NUM_OF_LEDS):
        led_button_array.append(tk.Button(app,bg='gray'))

    for i, bt in enumerate(led_button_array):
        bt['text'] = "" 
        bt['width'] = 10
        bt['height'] = 10
        bt['image'] = pixelVirtual
        bt['command'] = leddia(app, i,bt)
        bt.pack(side="left")

    app.protocol("WM_DELETE_WINDOW", on_closing)
    ok_button = tk.Button(app, text='Start', width=50, command=show_vis)
    ok_button.pack(side="bottom")

    
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
