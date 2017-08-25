import Tkinter
import random
import threading
import time


class App(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)

        self.status = False
        self.reverse = False
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.image = self.generate_image()

        self.c = Tkinter.Canvas(self, width=100, height=100)
        self.c.pack()
        self.i = self.c.create_image(0, 0, image=self.image, anchor=Tkinter.NW)

        self.btn = Tkinter.Button(self, text="start", command=self.start)
        self.btn.pack()

    def generate_image(self, image=None):
        if not image:
            image = Tkinter.PhotoImage(width=100, height=100)
        #self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        if not self.reverse:
            self.r += 2
        else:
            self.r -= 2

        if self.r > 255:
            self.r = 255
            self.reverse = True
        elif self.r < 0:
            self.r = 0
            self.reverse = False
        colors = [(self.r, self.r, self.r) for j in range(0, 10000)]
        row = 0
        col = 0
        for color in colors:
            image.put("#%02x%02x%02x" % color, (row, col))
            col += 1
            if col == 100:
                row += 1
                col = 0
        return image

    def start(self, *args):
        self.status = True

        thread = self.MyThread(self, self.c, self.i)
        thread.setDaemon(True)
        thread.start()

        self.btn["command"] = self.stop
        self.btn["text"] = "stop"

    def stop(self):
        self.status = False
        self.btn["command"] = self.start
        self.btn["text"] = "start"

    class MyThread(threading.Thread):
        def __init__(self, parent, canvas, image):
            threading.Thread.__init__(self)
            self.parent = parent
            self.c = canvas
            self.i = image

        def run(self):
            while self.parent.status:
                self.parent.image = self.parent.generate_image()
                self.c.itemconfigure(self.i, image=self.parent.image)


a = App()
a.mainloop()
