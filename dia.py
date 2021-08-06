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

class LedColorDia(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.color = None
        self.hexcolor = None
        try:
            super().__init__(parent, title)
        except: ## python 2.7 version. improve if you can.
            simpledialog.Dialog.__init__(self, parent, title)

    def body(self, frame):
        self.colorStringVar = tk.StringVar(frame, value="(0,0,0)")
        self.col_label = tk.Label(frame, width=25, text="Color")
        self.col_label.pack()
        self.col_box = tk.Entry(frame, width=25, textvariable = self.colorStringVar)
        self.col_box.pack()
        #self.col_box['show'] = '*'
        self.colorButton = tk.Button(frame, text = "col", command = self.choose)
        self.colorButton.pack()

        return frame

    def choose(self):
        self.allcolor = colorchooser.askcolor(title="Choose LED Color")
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


def leddia(app, i, buttoni):
    return lambda : mydialog(app, i, buttoni)

def mydialog(app, i, buttoni):
    dialog = LedColorDia(title="LED state %d"%i, parent=app)
    logging.info("Color on LED %d to be set to %s"%(i, dialog.color))
    buttoni['bg'] = dialog.hexcolor
    return dialog.color, dialog.hexcolor


