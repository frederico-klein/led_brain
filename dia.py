__metaclass__= type

import re
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

def textohex(color):
    colorliststr = re.sub(r"\(|\)| ","",color).split(",") 
    logging.info(colorliststr)
    colorlist = list(map(int,colorliststr))
    logging.info(colorlist)
    r = colorlist[0]
    g = colorlist[1]
    b = colorlist[2]
    hexcolor = '#%02x%02x%02x'%(r,g,b)
    return (r,g,b), hexcolor

class LedColorDia(simpledialog.Dialog):
    def __init__(self, parent, title, led):
        self.color = None
        self.hexcolor = None
        self.led = led
        try:
            super().__init__(parent, title)
        except: ## python 2.7 version. improve if you can.
            simpledialog.Dialog.__init__(self, parent, title)

    def body(self, frame):
        self.color = self.led.color
        self.hexcolor = textohex(self.color)[1]
        self.colorStringVar = tk.StringVar(frame, value=self.color)
        self.col_label = tk.Label(frame, width=25, text="Color")
        self.col_label.pack()
        self.col_box = tk.Entry(frame, width=25, textvariable = self.colorStringVar)
        self.col_box.pack()
        #self.col_box['show'] = '*'
        self.colorButton = tk.Button(frame, text = "Choose color", command = self.choose)
        self.colorButton.pack()

        return frame 

    def choose(self):
        self.allcolor = colorchooser.askcolor(title="Choose LED Color", color=self.hexcolor)               
        self.hexcolor = self.allcolor[1]
        self.r = self.allcolor[0][0]
        self.g = self.allcolor[0][1]
        self.b = self.allcolor[0][2]
        self.color ="(%d,%d,%d)"%(self.r,self.g,self.b)         
        self.colorStringVar.set(self.color)
        #self.col_box.insert(0,self.color)
        logging.info(self.color)

    def ok_pressed(self):
        # print("ok")
        self.color = self.col_box.get()
        ct, self.hexcolor =  textohex(self.color)
        self.r = ct[0]
        self.g = ct[1]
        self.b = ct[2]
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


def leddia(app, i, ledi):
    return lambda : mydialog(app, i, ledi)

def mydialog(app, i, ledi):
    dialog = LedColorDia(title="LED state %d"%i, parent=app, led= ledi)
    logging.info("Color on LED %d to be set to %s"%(i, dialog.color))
    ledi.setcolor(dialog.color)
    return dialog.color, dialog.hexcolor


