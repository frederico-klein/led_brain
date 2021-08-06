__metaclass__= type

import logging
import pygame, sys

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


class MyDialog(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.led_id = None
        self.color = None
        self.led_enabled = None
        #        super().__init__(parent, title)
        ##old style for compatibility
        try:
            super().__init__(parent, title)
        except: ## python 2.7 version. improve if you can.
            simpledialog.Dialog.__init__(self, parent, title)

    def body(self, frame):
        self.colorStringVar = tk.StringVar(frame, value="(0,0,0)")
 
        # print(type(frame)) # tkinter.Frame
        self.li_label = tk.Label(frame, width=25, text="Led Index")
        self.li_label.pack()
        self.li_box = tk.Entry(frame, width=25)
        self.li_box.pack()

        self.col_label = tk.Label(frame, width=25, text="Color")
        self.col_label.pack()
        self.col_box = tk.Entry(frame, width=25, textvariable = self.colorStringVar)
        self.col_box.pack()
        #self.col_box['show'] = '*'

        self.led_enable = tk.BooleanVar()
        self.chb = tk.Checkbutton(frame, text="LED enable", variable = self.led_enable)
        self.chb.pack()

        self.colorButton = tk.Button(frame, text = "col", command = self.choose)
        self.colorButton.pack()

        return frame

    def choose(self):
        color = colorchooser.askcolor(title="Choose LED Color")
        r = color[0][0]
        g = color[0][1]
        b = color[0][2]
        self.color ="(%d,%d,%d)"%(r,g,b) 
        self.colorStringVar.set(self.color)
        #self.col_box.insert(0,self.color)
        logging.info(self.color)

    def ok_pressed(self):
        # print("ok")
        self.led_id = self.li_box.get()
        self.color = self.col_box.get()
        self.led_enabled = self.led_enable.get()
        self.destroy()

    def cancel_pressed(self):
        # print("cancel")
        self.destroy()


    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            app.destroy()
            pygame.quit()
            sys.exit()
        except:
            pass

app = tk.Tk()

app.geometry("300x300")
app.title("Brain LEDS")
app.resizable(width=False,height=False)
#app.withdraw()
canvas = tk.Canvas(app, width = 180, height = 300)
canvas.pack()
img = tk.PhotoImage(file="logo32x32.png")
canvas.create_image(0,0,anchor=tk.NW, image = img)

app.protocol("WM_DELETE_WINDOW", on_closing)

app.update()

def mydialog(app):
    dialog = MyDialog(title="LED state", parent=app)
    return dialog.led_id, dialog.color, dialog.led_enabled 


