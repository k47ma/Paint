from tkinter import *
import tkColorChooser
from Tooltip import Tooltip

# constants for event status
SHIFT = 265
CAPS_LOCK = 266
CTRL = 268

# variables for configuration settings
COLOR = "#000000"
PENCIL_WIDTH = 1.0
BRUSH_WIDTH = 7.5
BRUSH_MODE = "circle"
ERASER_WIDTH = 20.0
ERASER_MODE = "circle"
LINE_WIDTH = 1.0
RECT_WIDTH = 1.0
CIRCLE_WIDTH = 1.0
FILL_COLOR = "#ffffff"


# top level class
class Paint(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.iconbitmap(r'image\paint.ico')
        self.wm_title("Paint")
        self.geometry("800x600")
        self.minsize(800, 600)

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
        pencil_btn = Button(self, image=self.pencil_img, cursor="hand2", command=lambda: self.select("pencil"))
        pencil_btn.pack(side=TOP)
        self.create_tooltip(pencil_btn, "pencil")
        self.types["pencil"] = pencil_btn
        self.cursors["pencil"] = "ul_angle"

        self.brush_img = PhotoImage(file="image\\brush.gif")
        brush_btn = Button(self, image=self.brush_img, cursor="hand2", command=lambda: self.select("brush"))
        brush_btn.pack(side=TOP)
        self.create_tooltip(brush_btn, "brush")
        self.types["brush"] = brush_btn
        self.cursors["brush"] = "target"

        self.eraser_img = PhotoImage(file="image\\eraser.gif")
        eraser_btn = Button(self, image=self.eraser_img, cursor="hand2", command=lambda: self.select("eraser"))
        eraser_btn.pack(side=TOP)
        self.create_tooltip(eraser_btn, "eraser")
        self.types["eraser"] = eraser_btn
        self.cursors["eraser"] = "target"

        self.line_img = PhotoImage(file="image\\line.gif")
        line_btn = Button(self, image=self.line_img, cursor="hand2", command=lambda: self.select("line"))
        line_btn.pack(side=TOP)
        self.create_tooltip(line_btn, "line")
        self.types["line"] = line_btn
        self.cursors["line"] = "plus"

        self.rect_img = PhotoImage(file="image\\rect.gif")
        rect_btn = Button(self, image=self.rect_img, cursor="hand2", command=lambda: self.select("rect"))
        rect_btn.pack(side=TOP)
        self.create_tooltip(rect_btn, "rectangle")
        self.types["rect"] = rect_btn
        self.cursors["rect"] = "tcross"

        self.oval_img = PhotoImage(file="image\\oval.gif")
        circle_btn = Button(self, image=self.oval_img, cursor="hand2", command=lambda: self.select("circle"))
        circle_btn.pack(side=TOP)
        self.create_tooltip(circle_btn, "oval")
        self.types["circle"] = circle_btn
        self.cursors["circle"] = "tcross"

        label1 = Label(self, text="Outline Color")
        label1.pack(side=TOP, pady=(6, 0))

        self.color_btn = Button(self, bg=FILL_COLOR, width=3, bd=1, relief=GROOVE, activebackground=FILL_COLOR,
                                command=self.select_color)
        self.color_btn.pack(side=TOP)

        label2 = Label(self, text="Fill Color")
        label2.pack(side=TOP, pady=(6, 0))

        self.fill_color_btn = Button(self, bg=COLOR, width=3, bd=1, relief=GROOVE, activebackground=COLOR,
                                     command=self.select_fill_color)
        self.fill_color_btn.pack(side=TOP)

        self.clear_img = PhotoImage(file="image\\cross.gif")
        clear_btn = Button(self, image=self.clear_img, cursor="hand2", command=lambda: self.canvas.clear())
        clear_btn.pack(side=BOTTOM)
        self.create_tooltip(clear_btn, "clear all")

        self.setting_frame = SettingFrame(self)
        self.setting_frame.pack(side=TOP, fill=BOTH, expand=True, ipady=6)

        self.select("pencil")
        self.setting_frame.show("pencil")

    def select(self, name):
        # deselect all the buttons and select target button
        for key in self.types:
            self.types[key]["relief"] = RAISED

        self.types[name]["relief"] = SUNKEN
        self.setting_frame.show(name)
        self.canvas["cursor"] = self.cursors[name]
        self.canvas.type = name

    def select_color(self):
        global COLOR
        selected_color = tkColorChooser.askcolor(COLOR, parent=self, title="Select Outline Color")
        if selected_color[1]:
            COLOR = selected_color[1]
            self.color_btn["bg"] = COLOR

    def select_fill_color(self):
        global FILL_COLOR
        selected_color = tkColorChooser.askcolor(FILL_COLOR, parent=self, title="Select Fill Color")
        if selected_color[1]:
            FILL_COLOR = selected_color[1]
            self.fill_color_btn["bg"] = FILL_COLOR

    def create_tooltip(self, widget, text):
        Tooltip(widget, text)


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
        self.create_line((self.lastX, self.lastY, event.x, event.y), fill=COLOR, width=PENCIL_WIDTH)
        self.lastX = event.x
        self.lastY = event.y

    def addBrushLine(self, event):
        r = BRUSH_WIDTH
        if BRUSH_MODE == "circle":
            self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill=COLOR, outline=COLOR)
        elif BRUSH_MODE == "square":
            self.create_rectangle((event.x - r, event.y - r, event.x + r, event.y + r), fill=COLOR, outline=COLOR)

    def addEraserLine(self, event):
        r = ERASER_WIDTH
        if ERASER_MODE == "circle":
            self.create_oval((event.x - r, event.y - r, event.x + r, event.y + r), fill="white", outline="white")
        elif ERASER_MODE == "square":
            self.create_rectangle((event.x - r, event.y - r, event.x + r, event.y + r), fill="white",
                                  outline="white")

    def addLine(self, event):
        if self.lastDraw:
            self.delete(self.lastDraw)

        if event.state == SHIFT:
            self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=COLOR, width=LINE_WIDTH)
        else:
            self.lastDraw = self.create_line((self.lastX, self.lastY, event.x, event.y), fill=COLOR, width=LINE_WIDTH)

    def addRect(self, event):
        if self.lastDraw:
            self.delete(self.lastDraw)

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
            self.lastDraw = self.create_rectangle(self.lastX, self.lastY, end_x, end_y, width=RECT_WIDTH, outline=COLOR,
                                                  fill=FILL_COLOR)
        else:
            # draw rectangle
            self.lastDraw = self.create_rectangle(self.lastX, self.lastY, event.x, event.y, width=RECT_WIDTH,
                                                  outline=COLOR, fill=FILL_COLOR)

    def addCircle(self, event):
        if self.lastDraw:
            self.delete(self.lastDraw)

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
            self.lastDraw = self.create_oval((self.lastX, self.lastY, end_x, end_y), width=CIRCLE_WIDTH, outline=COLOR,
                                             fill=FILL_COLOR)
        else:
            self.lastDraw = self.create_oval((self.lastX, self.lastY, event.x, event.y), width=CIRCLE_WIDTH,
                                             outline=COLOR, fill=FILL_COLOR)

    def setDraw(self, event):
        self.firstClick = True
        self.lastDraw = None

    def clear(self):
        self.delete("all")


# frame for containing tool settings
class SettingFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frames = {}

        pencil_frame = self.PencilFrame(self)
        pencil_frame.grid(row=0, column=0, sticky=NSEW)
        self.frames["pencil"] = pencil_frame

        brush_frame = self.BrushFrame(self)
        brush_frame.grid(row=0, column=0, sticky=NSEW)
        self.frames["brush"] = brush_frame

        eraser_frame = self.EraserFrame(self)
        eraser_frame.grid(row=0, column=0, sticky=NSEW)
        self.frames["eraser"] = eraser_frame

        line_frame = self.LineFrame(self)
        line_frame.grid(row=0, column=0, sticky=NSEW)
        self.frames["line"] = line_frame

        rect_frame = self.RectFrame(self)
        rect_frame.grid(row=0, column=0, sticky=NSEW)
        self.frames["rect"] = rect_frame

        circle_frame = self.CircleFrame(self)
        circle_frame.grid(row=0, column=0, sticky=NSEW)
        self.frames["circle"] = circle_frame

    def show(self, name):
        self.frames[name].lift()

    class PencilFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label = Label(self, text="Width")
            label.pack(side=TOP, pady=(6, 0))

            self.pencil_width = Scale(self, from_=5.0, to=1.0, resolution=0.1, sliderlength=25,
                                      command=self.set_pencil_width)
            self.pencil_width.set(PENCIL_WIDTH)
            self.pencil_width.pack(side=TOP)

        def set_pencil_width(self, event):
            global PENCIL_WIDTH
            PENCIL_WIDTH = self.pencil_width.get()

    class BrushFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.brush_width = Scale(self, from_=20.0, to=3.0, resolution=0.1, sliderlength=25,
                                     command=self.set_brush_width)
            self.brush_width.set(BRUSH_WIDTH)
            self.brush_width.pack(side=TOP)

            label2 = Label(self, text="Mode")
            label2.pack(side=TOP, pady=(6, 0))

            self.mode = StringVar()
            self.mode.set("circle")

            mode1 = Radiobutton(self, text=u"\u26ab", variable=self.mode, value="circle", command=self.set_brush_mode)
            mode2 = Radiobutton(self, text=u"\u25a0", variable=self.mode, value="square", command=self.set_brush_mode)
            mode1.pack(side=TOP)
            mode2.pack(side=TOP)

        def set_brush_width(self, event):
            global BRUSH_WIDTH
            BRUSH_WIDTH = self.brush_width.get()

        def set_brush_mode(self):
            global BRUSH_MODE
            BRUSH_MODE = self.mode.get()

    class EraserFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.eraser_width = Scale(self, from_=40.0, to=3.0, resolution=0.1, sliderlength=25,
                                      command=self.set_eraser_width)
            self.eraser_width.set(ERASER_WIDTH)
            self.eraser_width.pack(side=TOP)

            label2 = Label(self, text="Mode")
            label2.pack(side=TOP, pady=(6, 0))

            self.mode = StringVar()
            self.mode.set("circle")

            mode1 = Radiobutton(self, text=u"\u26ab", variable=self.mode, value="circle", command=self.set_eraser_mode)
            mode2 = Radiobutton(self, text=u"\u25a0", variable=self.mode, value="square", command=self.set_eraser_mode)
            mode1.pack(side=TOP)
            mode2.pack(side=TOP)

        def set_eraser_width(self, event):
            global ERASER_WIDTH
            ERASER_WIDTH = self.eraser_width.get()

        def set_eraser_mode(self):
            global ERASER_MODE
            ERASER_MODE = self.mode.get()

    class LineFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.line_width = Scale(self, from_=20.0, to=1.0, resolution=0.1, sliderlength=25,
                                    command=self.set_line_width)
            self.line_width.set(LINE_WIDTH)
            self.line_width.pack(side=TOP)

        def set_line_width(self, event):
            global LINE_WIDTH
            LINE_WIDTH = self.line_width.get()

    class RectFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.rect_width = Scale(self, from_=5.0, to=1.0, resolution=0.1, sliderlength=25,
                                    command=self.set_rect_width)
            self.rect_width.set(RECT_WIDTH)
            self.rect_width.pack(side=TOP)

        def set_rect_width(self, event):
            global RECT_WIDTH
            RECT_WIDTH = self.rect_width.get()

    class CircleFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.circle_width = Scale(self, from_=5.0, to=1.0, resolution=0.1, sliderlength=25,
                                      command=self.set_circle_width)
            self.circle_width.set(CIRCLE_WIDTH)
            self.circle_width.pack(side=TOP)

        def set_circle_width(self, event):
            global CIRCLE_WIDTH
            CIRCLE_WIDTH = self.circle_width.get()


paint = Paint()
paint.mainloop()
