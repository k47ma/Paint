from tkinter import *


# constants for event status
SHIFT = 265
CAPS_LOCK = 266
CTRL = 268


# top level class
class Paint(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.wm_title("Paint")

        canvas_panel = PaintCanvas(self)
        control_frame = ControlFrame(self, canvas_panel)
        control_frame.pack(side=LEFT, fill=Y, expand=False, padx=6, pady=5)
        canvas_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)


# frame for control buttons
class ControlFrame(Frame):
    def __init__(self, parent, canvas):
        Frame.__init__(self, parent)

        self.canvas = canvas
        self.types = {}
        self.cursors = {}

        pencil_btn = Button(self, text="pencil", command=lambda: self.select("pencil"))
        pencil_btn.pack(side=TOP, pady=5)
        self.types["pencil"] = pencil_btn
        self.cursors["pencil"] = "ul_angle"

        eraser_btn = Button(self, text="eraser", command=lambda: self.select("eraser"))
        eraser_btn.pack(side=TOP, pady=5)
        self.types["eraser"] = eraser_btn
        self.cursors["eraser"] = "target"

        line_btn = Button(self, text="line", command=lambda: self.select("line"))
        line_btn.pack(side=TOP, pady=5)
        self.types["line"] = line_btn
        self.cursors["line"] = "plus"

        rect_btn = Button(self, text="rect", command=lambda: self.select("rect"))
        rect_btn.pack(side=TOP, pady=5)
        self.types["rect"] = rect_btn
        self.cursors["rect"] = "tcross"

        circle_btn = Button(self, text="circle", command=lambda: self.select("circle"))
        circle_btn.pack(side=TOP, pady=5)
        self.types["circle"] = circle_btn
        self.cursors["circle"] = "tcross"

        clear_btn = Button(self, text="clear", command=lambda: self.canvas.clear())
        clear_btn.pack(side=TOP, pady=5)

        self.select("pencil")

    def select(self, name):
        # deselect all the buttons and select target button
        for key in self.types:
            self.types[key]["relief"] = RAISED

        self.types[name]["relief"] = SUNKEN
        self.canvas["cursor"] = self.cursors[name]
        self.canvas.type = name


# frame for canvas
class PaintCanvas(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent, bg="white")

        self.lastX = 0
        self.lastY = 0
        self.firstClick = True
        self.lastDraw = None

        self.bind("<Button-1>", self.startDraw)
        self.bind("<B1-Motion>", self.addLine)
        self.bind("<ButtonRelease-1>", self.setDraw)

    def startDraw(self, event):
        if self.firstClick:
            self.lastX, self.lastY = event.x, event.y
            self.firstClick = False

    def addLine(self, event):
        if self.lastDraw:
            self.delete(self.lastDraw)

        if self.type == "pencil":
            self.create_line((self.lastX, self.lastY, event.x, event.y), activefill="blue")
            self.lastX = event.x
            self.lastY = event.y
        elif self.type == "eraser":
            r = 20.0
            self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill="white", outline="white")
        elif self.type == "line":
            if event.state == SHIFT:
                self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y))
            else:
                self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y))
        elif self.type == "rect":
            if event.state == SHIFT:
                side = min(abs(self.lastX - event.x), abs(self.lastY - event.y))

                # determine the direction of endpoint
                if event.x - self.lastX >= 0:
                    dir_x = 1
                else:
                    dir_x = -1

                if event.y - self.lastY >= 0:
                    dir_y = 1
                else:
                    dir_y = -1

                # draw square
                end_x = self.lastX + dir_x * side
                end_y = self.lastY + dir_y * side
                self.lastDraw = self.create_rectangle(self.lastX, self.lastY, end_x, end_y)
            else:
                #draw rectangle
                self.lastDraw = self.create_rectangle(self.lastX, self.lastY, event.x, event.y)
        elif self.type == "circle":
            if event.state == SHIFT:
                diameter = min(abs(self.lastX - event.x), abs(self.lastY - event.y))

                # determine the direction of endpoint
                if event.x - self.lastX >= 0:
                    dir_x = 1
                else:
                    dir_x = -1

                if event.y - self.lastY >= 0:
                    dir_y = 1
                else:
                    dir_y = -1

                # draw circle
                end_x = self.lastX + dir_x * diameter
                end_y = self.lastY + dir_y * diameter
                self.lastDraw = self.create_oval((self.lastX, self.lastY, end_x, end_y))
            else:
                self.lastDraw = self.create_oval((self.lastX, self.lastY, event.x, event.y))

    def setDraw(self, event):
        self.firstClick = True
        self.lastDraw = None

    def clear(self):
        self.delete("all")


paint = Paint()
paint.mainloop()
