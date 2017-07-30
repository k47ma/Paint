from tkinter import Toplevel, Label


class Tooltip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.root = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event):
        x, y, cx, cy = self.widget.bbox()
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 3

        self.root = Toplevel(self.widget)
        self.root.wm_overrideredirect(True)
        self.root.wm_geometry("+%d+%d" % (x, y))

        label = Label(self.root, text=self.text, justify="left", bg="white", relief="solid", bd=1, font=("time", 9))
        label.pack(ipadx=1)

    def leave(self, event):
        if self.root:
            self.root.destroy()
