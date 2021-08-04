try:
    # for Python2
    import Tkinter as tk   ## notice capitalized T in Tkinter 
    import ttk
    import tkSimpleDialog as simpledialog
except ImportError:
    # for Python3
    import tkinter as tk   ## notice lowercase 't' in tkinter here
    from tkinter import ttk
    from tkinter import simpledialog



class MyDialog(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.my_username = None
        self.my_password = None
        super().__init__(parent, title)

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        self.my_username_label = tk.Label(frame, width=25, text="Username")
        self.my_username_label.pack()
        self.my_username_box = tk.Entry(frame, width=25)
        self.my_username_box.pack()

        self.my_password_label = tk.Label(frame, width=25, text="Password")
        self.my_password_label.pack()
        self.my_password_box = tk.Entry(frame, width=25)
        self.my_password_box.pack()
        self.my_password_box['show'] = '*'

        return frame

    def ok_pressed(self):
        # print("ok")
        self.my_username = self.my_username_box.get()
        self.my_password = self.my_password_box.get()
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


app = tk.Tk()

def mydialog(app):
    dialog = MyDialog(title="Login", parent=app)
    return dialog.my_username, dialog.my_password


