from tkinter import *
from config import *
from math import *


# frame for canvas
class PaintCanvas(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent, bg="white")

        self.lastX = 0
        self.lastY = 0
        self.firstClick = True
        self.history = []
        self.action = []
        self.entry = None
        self.controller = None

        self.bind("<Button-1>", self.startDraw)
        self.bind("<Motion>", self.printMousePosition)
        self.bind("<B1-Motion>", self.draw)
        self.bind("<ButtonRelease-1>", self.setDraw)

    def printMousePosition(self, event):
        if self.controller:
            self.controller.printMousePosition(event)

    def startDraw(self, event):
        self.focus_force()
        if self.firstClick:
            self.lastX, self.lastY = event.x, event.y
            self.firstClick = False
        if self.type == "text" and self.entry:
            self.entry.draw_text()
        self.draw(event)

    def draw(self, event):
        self.printMousePosition(event)

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
        elif type == "text":
            self.addDashRect(event)

    def addPencilLine(self, event):
        line = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=settings["COLOR"],
                                width=settings["PENCIL_WIDTH"])
        self.action.append(line)
        self.lastX = event.x
        self.lastY = event.y

    def addBrushLine(self, event):
        r = settings["BRUSH_WIDTH"]
        if settings["BRUSH_MODE"] == "circle":
            oval = self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill=settings["COLOR"],
                                    outline=settings["COLOR"])
            self.action.append(oval)
        elif settings["BRUSH_MODE"] == "square":
            oval = self.create_rectangle((event.x - r, event.y - r, event.x + r, event.y + r), fill=settings["COLOR"],
                                         outline=settings["COLOR"])
            self.action.append(oval)

    def addEraserLine(self, event):
        r = settings["ERASER_WIDTH"]
        if settings["ERASER_MODE"] == "circle":
            erase = self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill="white",
                                     outline="white")
            self.action.append(erase)
        elif settings["ERASER_MODE"] == "square":
            erase = self.create_rectangle((event.x - r, event.y - r, event.x + r, event.y + r), fill="white",
                                          outline="white")
            self.action.append(erase)

    def addLine(self, event):
        if self.action:
            self.delete(self.action[0])

        if event.state == SHIFT:
            # avoid "divided by 0" error
            if event.x == self.lastX:
                line = self.create_line((self.lastX, self.lastY, self.lastX, event.y),
                                        fill=settings["COLOR"], width=settings["LINE_WIDTH"],
                                        capstyle=ROUND)
                self.action = [line]
                return

            slope = float((event.y - self.lastY) / (event.x - self.lastX))

            if slope >= tan(radians(67.5)) or slope < tan(radians(112.5)):
                line = self.create_line((self.lastX, self.lastY, self.lastX, event.y),
                                        fill=settings["COLOR"], width=settings["LINE_WIDTH"],
                                        capstyle=ROUND)
            elif tan(radians(-22.5)) <= slope < tan(radians(22.5)):
                line = self.create_line((self.lastX, self.lastY, event.x, self.lastY),
                                        fill=settings["COLOR"], width=settings["LINE_WIDTH"],
                                        capstyle=ROUND)
            elif tan(radians(22.5)) <= slope < tan(radians(67.5)):
                end_x = int(round((self.lastX + event.x - self.lastY + event.y) / 2))
                end_y = int(round((event.x - self.lastX + event.y + self.lastY) / 2))
                line = self.create_line((self.lastX, self.lastY, end_x, end_y), fill=settings["COLOR"],
                                        width=settings["LINE_WIDTH"], capstyle=ROUND)
            else:
                end_x = int(round((self.lastX + event.x + self.lastY - event.y) / 2))
                end_y = int(round((self.lastX - event.x + self.lastY + event.y) / 2))
                line = self.create_line((self.lastX, self.lastY, end_x, end_y), fill=settings["COLOR"],
                                        width=settings["LINE_WIDTH"], capstyle=ROUND)
        else:
            line = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=settings["COLOR"],
                                    width=settings["LINE_WIDTH"], capstyle=ROUND)
        self.action = [line]

    def addRect(self, event):
        if self.action:
            self.delete(self.action[0])

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
            rect = self.create_rectangle(self.lastX, self.lastY, end_x, end_y, width=settings["RECT_WIDTH"],
                                         outline=settings["COLOR"],
                                         fill=fill_color)
        else:
            # draw rectangle
            rect = self.create_rectangle(self.lastX, self.lastY, event.x, event.y,
                                         width=settings["RECT_WIDTH"],
                                         outline=settings["COLOR"], fill=fill_color)
        self.action = [rect]

    def addCircle(self, event):
        if self.action:
            self.delete(self.action[0])

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
            oval = self.create_oval((self.lastX, self.lastY, end_x, end_y), width=settings["CIRCLE_WIDTH"],
                                    outline=settings["COLOR"],
                                    fill=fill_color)
        else:
            oval = self.create_oval((self.lastX, self.lastY, event.x, event.y), width=settings["CIRCLE_WIDTH"],
                                    outline=settings["COLOR"], fill=fill_color)
        self.action = [oval]

    def addDashRect(self, event):
        if self.action:
            self.delete(self.action[0])

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
            rect = self.create_rectangle(self.lastX, self.lastY, end_x, end_y, outline="black", fill="white",
                                         dash=[3, 3])
        else:
            # draw rectangle
            rect = self.create_rectangle(self.lastX, self.lastY, event.x, event.y, outline="black", fill="white",
                                         dash=[3, 3])
        self.action = [rect]

    def revert(self, event=None):
        try:
            last_action = self.history.pop()
        except IndexError:
            return

        for action in last_action:
            self.delete(action)

    def setDraw(self, event=None):
        if self.type == "text":
            try:
                (x1, y1, x2, y2) = self.coords(self.action[0])
            except IndexError:
                return

            width = abs(x1 - x2)
            height = abs(y1 - y2)

            char_width = int(width // 7)
            char_height = int(height // 15)

            if char_width < 10:
                char_width = 10

            self.delete(self.action[0])

            paint_text = self.PaintText(self, x1, y1, char_width, char_height)
            paint_text.place(x=x1, y=y1, anchor=NW)
        else:
            self.history.append(self.action)

        self.firstClick = True
        self.action = []

    def clear(self):
        self.delete("all")

    class PaintText(Text):
        def __init__(self, canvas, x, y, width, height):
            Text.__init__(self, canvas, relief=SOLID, width=width, height=height, wrap=WORD, bd=1,
                          fg=settings["TEXT_COLOR"])
            self.width = width
            self.height = height
            self.canvas = canvas
            self.x = x
            self.y = y
            self["font"] = self.get_font()

            if not settings["TRANSPARENT"]:
                self["bg"] = settings["FILL_COLOR"]

            self.focus()
            self.bind("<FocusOut>", self.draw_text)
            self.bind("<Key-Return>", self.draw_text)
            self.bind("<Control-Return>", lambda x: self.insert(INSERT, ""))

        def draw_text(self, *args):
            background = None

            # draw the background of text
            if not settings["TRANSPARENT"]:
                x1 = self.x
                y1 = self.y
                x2 = x1 + self.width * 7
                y2 = y1 + self.height * 15

                background = self.canvas.create_rectangle((x1, y1, x2, y2), outline=settings["COLOR"],
                                                          fill=settings["FILL_COLOR"])

            text = self.get(1.0, END)
            draw = self.canvas.create_text(self.x + 3, self.y - 2, text=text, anchor=NW, font=self.get_font(),
                                           width=self.width * 7, fill=settings["TEXT_COLOR"])

            if not settings["TRANSPARENT"]:
                self.canvas.history.append([draw, background])
            else:
                self.canvas.history.append([draw])

            self.canvas.entry = None
            self.destroy()

        def get_font(self):
            font_family = settings["FONT_FAMILY"]
            font_size = settings["FONT_SIZE"]
            font_decoration_list = []

            if settings["BOLD"]:
                font_decoration_list.append("bold")
            if settings["SLANT"]:
                font_decoration_list.append("italic")
            if settings["UNDERLINE"]:
                font_decoration_list.append("underline")
            if settings["OVERSTRIKE"]:
                font_decoration_list.append("overstrike")

            font_decoration = " ".join(font_decoration_list)

            return (font_family, font_size, font_decoration)
