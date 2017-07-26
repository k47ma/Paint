from tkinter import *
import tkColorChooser


# constants for event status
SHIFT = 265
CAPS_LOCK = 266
CTRL = 268

COLOR = "#000000"


# top level class
class Paint(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.iconbitmap(r'image\paint.ico')
        self.wm_title("Paint")
        self.geometry("700x500")
        self.minsize(700, 500)

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

        self.pencil_img = PhotoImage(file="image\\pencil.gif")
        pencil_btn = Button(self, image=self.pencil_img, command=lambda: self.select("pencil"))
        pencil_btn.pack(side=TOP)
        self.types["pencil"] = pencil_btn
        self.cursors["pencil"] = "ul_angle"

        self.brush_img = PhotoImage(file="image\\brush.gif")
        brush_img = Button(self, image=self.brush_img, command=lambda: self.select("brush"))
        brush_img.pack(side=TOP)
        self.types["brush"] = brush_img
        self.cursors["brush"] = "target"

        self.eraser_img = PhotoImage(file="image\\eraser.gif")
        eraser_btn = Button(self, image=self.eraser_img, command=lambda: self.select("eraser"))
        eraser_btn.pack(side=TOP)
        self.types["eraser"] = eraser_btn
        self.cursors["eraser"] = "target"

        self.line_img = PhotoImage(file="image\\line.gif")
        line_btn = Button(self, image=self.line_img, command=lambda: self.select("line"))
        line_btn.pack(side=TOP)
        self.types["line"] = line_btn
        self.cursors["line"] = "plus"

        self.rect_img = PhotoImage(file="image\\rect.gif")
        rect_btn = Button(self, image=self.rect_img, command=lambda: self.select("rect"))
        rect_btn.pack(side=TOP)
        self.types["rect"] = rect_btn
        self.cursors["rect"] = "tcross"

        self.oval_img = PhotoImage(file="image\\oval.gif")
        circle_btn = Button(self, image=self.oval_img, command=lambda: self.select("circle"))
        circle_btn.pack(side=TOP)
        self.types["circle"] = circle_btn
        self.cursors["circle"] = "tcross"

        self.color_img = PhotoImage(file="image\\colors.gif")
        color_btn = Button(self, image=self.color_img, command=self.selectColor)
        color_btn.pack(side=TOP, pady=6)

        self.clear_img = PhotoImage(file="image\\cross.gif")
        clear_btn = Button(self, image=self.clear_img, command=lambda: self.canvas.clear())
        clear_btn.pack(side=BOTTOM)

        self.select("pencil")

    def select(self, name):
        # deselect all the buttons and select target button
        for key in self.types:
            self.types[key]["relief"] = RAISED

        self.types[name]["relief"] = SUNKEN
        self.canvas["cursor"] = self.cursors[name]
        self.canvas.type = name

    def selectColor(self):
        global COLOR
        selected_color = tkColorChooser.askcolor(COLOR, parent=self, title="Color Selector")
        if selected_color[1]:
            COLOR = selected_color[1]


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
            self.create_line((self.lastX, self.lastY, event.x, event.y), fill=COLOR)
            self.lastX = event.x
            self.lastY = event.y
        elif self.type == "brush":
            r = 7.5
            self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill=COLOR, outline=COLOR)
        elif self.type == "eraser":
            r = 20.0
            self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill="white", outline="white")
        elif self.type == "line":
            if event.state == SHIFT:
                self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=COLOR)
            else:
                self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=COLOR)
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
                self.lastDraw = self.create_rectangle(self.lastX, self.lastY, end_x, end_y, outline=COLOR)
            else:
                #draw rectangle
                self.lastDraw = self.create_rectangle(self.lastX, self.lastY, event.x, event.y, outline=COLOR)
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
                self.lastDraw = self.create_oval((self.lastX, self.lastY, end_x, end_y), outline=COLOR)
            else:
                self.lastDraw = self.create_oval((self.lastX, self.lastY, event.x, event.y), outline=COLOR)

    def setDraw(self, event):
        self.firstClick = True
        self.lastDraw = None

    def clear(self):
        self.delete("all")


paint = Paint()
paint.mainloop()
