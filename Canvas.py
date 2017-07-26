from tkinter import *
from config import *


# frame for canvas
class PaintCanvas(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent, bg="white")

        self.lastX = 0
        self.lastY = 0
        self.firstClick = True
        self.lastDraw = None

        self.bind("<Button-1>", self.startDraw)
        self.bind("<B1-Motion>", self.draw)
        self.bind("<ButtonRelease-1>", self.setDraw)

    def startDraw(self, event):
        if self.firstClick:
            self.lastX, self.lastY = event.x, event.y
            self.firstClick = False

    def draw(self, event):
        type = self.type
        if type == "pencil":
            self.addPencilLine(event)
        elif type == "brush":
            self.addBrushLine(event)
        elif type == "eraser":
            self.addEraserLine(event)
        elif type == "line":
            self.addLine(event)
        elif type == "rect":
            self.addRect(event)
        elif type == "circle":
            self.addCircle(event)

    def addPencilLine(self, event):
        self.create_line((self.lastX, self.lastY, event.x, event.y), fill=settings["COLOR"],
                         width=settings["PENCIL_WIDTH"])
        self.lastX = event.x
        self.lastY = event.y

    def addBrushLine(self, event):
        r = settings["BRUSH_WIDTH"]
        if settings["BRUSH_MODE"] == "circle":
            self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill=settings["COLOR"],
                             outline=settings["COLOR"])
        elif settings["BRUSH_MODE"] == "square":
            self.create_rectangle((event.x - r, event.y - r, event.x + r, event.y + r), fill=settings["COLOR"],
                                  outline=settings["COLOR"])

    def addEraserLine(self, event):
        r = settings["ERASER_WIDTH"]
        if settings["ERASER_MODE"] == "circle":
            self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill="white", outline="white")
        elif settings["ERASER_MODE"] == "square":
            self.create_rectangle((event.x - r, event.y - r, event.x + r, event.y + r), fill="white",
                                  outline="white")

    def addLine(self, event):
        if self.lastDraw:
            self.delete(self.lastDraw)

        if event.state == SHIFT:
            self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=settings["COLOR"],
                                             width=settings["LINE_WIDTH"])
        else:
            self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=settings["COLOR"],
                                             width=settings["LINE_WIDTH"])

    def addRect(self, event):
        if self.lastDraw:
            self.delete(self.lastDraw)

        if settings["TRANSPARENT"]:
            fill_color = ""
        else:
            fill_color = settings["FILL_COLOR"]

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
            self.lastDraw = self.create_rectangle(self.lastX, self.lastY, end_x, end_y, width=settings["RECT_WIDTH"],
                                                  outline=settings["COLOR"],
                                                  fill=fill_color)
        else:
            # draw rectangle
            self.lastDraw = self.create_rectangle(self.lastX, self.lastY, event.x, event.y,
                                                  width=settings["RECT_WIDTH"],
                                                  outline=settings["COLOR"], fill=fill_color)

    def addCircle(self, event):
        if self.lastDraw:
            self.delete(self.lastDraw)

        if settings["TRANSPARENT"]:
            fill_color = ""
        else:
            fill_color = settings["FILL_COLOR"]

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
            self.lastDraw = self.create_oval((self.lastX, self.lastY, end_x, end_y), width=settings["CIRCLE_WIDTH"],
                                             outline=settings["COLOR"],
                                             fill=fill_color)
        else:
            self.lastDraw = self.create_oval((self.lastX, self.lastY, event.x, event.y), width=settings["CIRCLE_WIDTH"],
                                             outline=settings["COLOR"], fill=fill_color)

    def setDraw(self, event):
        self.firstClick = True
        self.lastDraw = None

    def clear(self):
        self.delete("all")
