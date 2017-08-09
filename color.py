import Tkinter
import random
import threading


class App:
    def __init__(self, t):
        self.image = self.generate_image()
        self.c = Tkinter.Canvas(t, width=100, height=100)
        self.c.pack()
        self.i = self.c.create_image(0, 0, image=self.image, anchor=Tkinter.NW)

        btn = Tkinter.Button(t, text="start", command=self.start)
        btn.pack()

    def generate_image(self):
        image = Tkinter.PhotoImage(width=100, height=100)
        colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(0, 10000)]
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
        thread = self.MyThread(self, self.c, self.i)
        thread.setDaemon(True)
        thread.start()

    class MyThread(threading.Thread):
        def __init__(self, parent, canvas, image):
            threading.Thread.__init__(self)
            self.parent = parent
            self.c = canvas
            self.i = image

        def run(self):
            while True:
                self.image = self.parent.generate_image()
                self.c.itemconfigure(self.i, image=self.image)

t = Tkinter.Tk()
a = App(t)
t.mainloop()
