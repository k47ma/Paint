import Tkinter
import random
import time


class App(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)

        self.status = False
        self.reverse = False
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.x = random.randint(0, 99)
        self.y = random.randint(0, 99)
        self.boat = Tkinter.PhotoImage(file="image\\boat.gif")
        self.origin_x = 50
        self.origin_y = 50
        self.image = self.generate_image()

        self.c = Tkinter.Canvas(self, width=100, height=100)
        self.c.pack()
        self.i = self.c.create_image(0, 0, image=self.image, anchor=Tkinter.NW)
        self.boat_position = self.c.create_image(self.x, self.y, image=self.boat, anchor=Tkinter.CENTER)

        self.btn = Tkinter.Button(self, width=6, text="start", command=self.start)
        self.btn.pack(pady=5)

        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)
        self.c.bind("<Button-1>", self.set_origin)
        self.c.bind("<B1-Motion>", self.set_origin)
        self.bind("<Return>", self.check_position)

        self.update_image()

    def move_down(self, event):
        if self.origin_y < 99:
            self.origin_y += 1

    def move_up(self, event):
        if self.origin_y > 2:
            self.origin_y -= 1

    def move_left(self, event):
        if self.origin_x > 1:
            self.origin_x -= 1

    def move_right(self, event):
        if self.origin_x < 99:
            self.origin_x += 1

    def set_origin(self, event):
        self.origin_x = event.x
        self.origin_y = event.y

    def check_position(self, event):
        if self.origin_x - 5 <= self.x <= self.origin_x + 5 and self.origin_y - 5 <= self.y <= self.origin_y + 5:
            # delete the old boat and generate a new one
            self.c.delete(self.boat_position)
            self.x = random.randint(0, 99)
            self.y = random.randint(0, 99)
            self.boat_position = self.c.create_image(self.x, self.y, image=self.boat, anchor=Tkinter.CENTER)
            print "Target eliminated!"
        else:
            print "Target missed!"

    def generate_image(self):
        image = Tkinter.PhotoImage(width=100, height=100)
        r = self.r
        row = 0
        col = 0
        for i in range(10000):
            image.put("#%02x%02x%02x" % (r, r, r), (row, col))
            row += 1
            if row == 100:
                col += 1
                row = 0
        return image

    def update_image(self):
        image = self.image.copy()
        #self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)

        color = (self.r, self.r, self.r)

        if self.reverse:
            self.r -= 2
        else:
            self.r += 2

        if self.r > 255:
            self.r = 255
            self.reverse = True
        elif self.r < 0:
            self.r = 0
            self.reverse = False

        for x in range(100):
            for y in range(100):
                if (x == self.origin_x - 5 or x == self.origin_x + 5) and self.origin_y - 5 <= y <= self.origin_y + 5:
                    image.put("#00ff00", (x, y))
                elif (y == self.origin_y - 5 or y == self.origin_y + 5) and self.origin_x - 5 <= x <= self.origin_x + 5:
                    image.put("#00ff00", (x, y))
                elif x == self.origin_x or y == self.origin_y:
                    image.put("#00ff00", (x, y))
                else:
                    image.put("#%02x%02x%02x" % color, (x, y))

        self.image = image
        self.c.itemconfigure(self.i, image=self.image)

        if self.status:
            self.after(1, self.update_image)

    def start(self, *args):
        self.status = True
        self.update_image()

        self.btn["command"] = self.stop
        self.btn["text"] = "stop"

    def stop(self):
        self.status = False
        self.btn["command"] = self.start
        self.btn["text"] = "start"


a = App()
a.mainloop()
