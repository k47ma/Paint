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
        self.x = 0
        self.y = 0
        self.origin = 50
        self.image = self.generate_image()

        self.c = Tkinter.Canvas(self, width=100, height=100)
        self.c.pack()
        self.i = self.c.create_image(0, 0, image=self.image, anchor=Tkinter.NW)

        self.btn = Tkinter.Button(self, text="start", command=self.start)
        self.btn.pack()

        self.bind("<Up>", self.increase_origin)
        self.bind("<Down>", self.decrease_origin)

    def increase_origin(self, event):
        if self.origin > 2:
            self.origin -= 1

    def decrease_origin(self, event):
        if self.origin < 99:
            self.origin += 1

    def generate_image(self):
        image = Tkinter.PhotoImage(width=100, height=100)
        r = self.r
        row = 0
        col = 0
        for i in range(10000):
            image.put("#%02x%02x%02x" % (r, r, r), (row, col))
        return image

    def update_image(self, image=None):
        image = self.image.copy()
        #self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)

        color = (self.r, self.r, self.r)

        self.x += 1

        if self.x == 100:
            self.x = 0

            if not self.reverse:
                self.r += 5
            else:
                self.r -= 5

            if self.r > 255:
                self.r = 255
                self.reverse = True
            elif self.r < 0:
                self.r = 0
                self.reverse = False

        for y in range(100):
            if y == self.origin:
                image.put("#00ff00", (self.x, y))
            else:
                image.put("#%02x%02x%02x" % color, (self.x, y))
            if self.x+1 < 100:
                image.put("#00ff00", (self.x+1, y))
            else:
                image.put("#00ff00", (0, y))
        self.image = image

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
                self.parent.update_image()
                self.c.itemconfigure(self.i, image=self.parent.image)
                time.sleep(0.01)


a = App()
a.mainloop()
