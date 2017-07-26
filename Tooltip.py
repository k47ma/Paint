from threading import Thread
from time import sleep
from tkinter import Toplevel, Label


class Tooltip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.thread = None
        self.root = None
        self.widget.bind("<Enter>", self.tooltip_thread_start)
        self.widget.bind("<Leave>", self.destroy_tooltip)

    def tooltip_thread_start(self, event):
        self.thread = TooltipThread(self.widget, self.text, self)
        self.thread.daemon = True
        self.thread.run()

    def tooltip_thread_stop(self):
        self.thread.cancelled = True

    def destroy_tooltip(self, event):
        if self.root:
            self.root.destroy()


class TooltipThread(Thread):
    def __init__(self, widget, text, parent):
        Thread.__init__(self)

        self.widget = widget
        self.text = text
        self.parent = parent
        self.cancelled = False

    def run(self):
        sleep(0.6)

        if not self.cancelled:
            self.create_tooltip()

    def create_tooltip(self):
        x, y, cx, cy = self.widget.bbox()
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.parent.root = Toplevel(self.widget)
        self.parent.root.wm_overrideredirect(True)
        self.parent.root.wm_geometry("+%d+%d" % (x, y))

        label = Label(self.parent.root, text=self.text, justify="left", bg="yellow", relief="solid", bd=1, font=("time", 9))
        label.pack()
