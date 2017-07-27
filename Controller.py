from tkinter import *
from Tooltip import *
from config import *
import tkColorChooser


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

        self.revert_img = PhotoImage(file="image\\revert.gif")
        revert_btn = Button(self, image=self.revert_img, cursor="hand2", command=self.canvas.revert)
        revert_btn.pack(side=TOP, pady=6)
        self.create_tooltip(revert_btn, "revert")

        label1 = Label(self, text="Outline Color")
        label1.pack(side=TOP, pady=(6, 0))

        self.color_btn = Button(self, bg=settings["COLOR"], width=3, bd=1, relief=GROOVE,
                                activebackground=settings["COLOR"],
                                command=self.select_color)
        self.color_btn.pack(side=TOP)

        label2 = Label(self, text="Fill Color")
        label2.pack(side=TOP, pady=(6, 0))

        self.fill_color_btn = Button(self, bg=settings["FILL_COLOR"], width=3, bd=1, relief=GROOVE,
                                     activebackground=settings["FILL_COLOR"],
                                     command=self.select_fill_color)
        self.fill_color_btn.pack(side=TOP)

        self.transparency_var = IntVar()
        self.transparency_var.set(1)
        self.transparency = Checkbutton(self, text="Transparent Fill", variable=self.transparency_var,
                                        command=self.set_transparency)
        self.transparency.pack(side=TOP)

        self.clear_img = PhotoImage(file="image\\cross.gif")
        clear_btn = Button(self, image=self.clear_img, cursor="hand2", command=self.canvas.clear)
        clear_btn.pack(side=BOTTOM, pady=10)
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
        selected_color = tkColorChooser.askcolor(settings["COLOR"], parent=self, title="Select Outline Color")
        if selected_color[1]:
            settings["COLOR"] = selected_color[1]
            self.color_btn["bg"] = settings["COLOR"]

    def select_fill_color(self):
        selected_color = tkColorChooser.askcolor(settings["FILL_COLOR"], parent=self, title="Select Fill Color")
        if selected_color[1]:
            settings["FILL_COLOR"] = selected_color[1]
            self.fill_color_btn["bg"] = settings["FILL_COLOR"]

    def set_transparency(self):
        settings["TRANSPARENT"] = bool(self.transparency_var.get())

    def create_tooltip(self, widget, text):
        Tooltip(widget, text)


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
            self.pencil_width.set(settings["PENCIL_WIDTH"])
            self.pencil_width.pack(side=TOP)

        def set_pencil_width(self, event):
            settings["PENCIL_WIDTH"] = self.pencil_width.get()

    class BrushFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.brush_width = Scale(self, from_=20.0, to=3.0, resolution=0.1, sliderlength=25,
                                     command=self.set_brush_width)
            self.brush_width.set(settings["BRUSH_WIDTH"])
            self.brush_width.pack(side=TOP)

            label2 = Label(self, text="Shape")
            label2.pack(side=TOP, pady=(6, 0))

            self.mode = StringVar()
            self.mode.set("circle")

            mode1 = Radiobutton(self, text=u"\u26ab", variable=self.mode, value="circle", command=self.set_brush_mode)
            mode2 = Radiobutton(self, text=u"\u25a0", variable=self.mode, value="square", command=self.set_brush_mode)
            mode1.pack(side=TOP)
            mode2.pack(side=TOP)

        def set_brush_width(self, event):
            settings["BRUSH_WIDTH"] = self.brush_width.get()

        def set_brush_mode(self):
            settings["BRUSH_MODE"] = self.mode.get()

    class EraserFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.eraser_width = Scale(self, from_=40.0, to=3.0, resolution=0.1, sliderlength=25,
                                      command=self.set_eraser_width)
            self.eraser_width.set(settings["ERASER_WIDTH"])
            self.eraser_width.pack(side=TOP)

            label2 = Label(self, text="Shape")
            label2.pack(side=TOP, pady=(6, 0))

            self.mode = StringVar()
            self.mode.set("circle")

            mode1 = Radiobutton(self, text=u"\u26ab", variable=self.mode, value="circle", command=self.set_eraser_mode)
            mode2 = Radiobutton(self, text=u"\u25a0", variable=self.mode, value="square", command=self.set_eraser_mode)
            mode1.pack(side=TOP)
            mode2.pack(side=TOP)

        def set_eraser_width(self, event):
            settings["ERASER_WIDTH"] = self.eraser_width.get()

        def set_eraser_mode(self):
            settings["ERASER_MODE"] = self.mode.get()

    class LineFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.line_width = Scale(self, from_=20.0, to=1.0, resolution=0.1, sliderlength=25,
                                    command=self.set_line_width)
            self.line_width.set(settings["LINE_WIDTH"])
            self.line_width.pack(side=TOP)

        def set_line_width(self, event):
            settings["LINE_WIDTH"] = self.line_width.get()

    class RectFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.rect_width = Scale(self, from_=5.0, to=1.0, resolution=0.1, sliderlength=25,
                                    command=self.set_rect_width)
            self.rect_width.set(settings["RECT_WIDTH"])
            self.rect_width.pack(side=TOP)

        def set_rect_width(self, event):
            settings["RECT_WIDTH"] = self.rect_width.get()

    class CircleFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)

            label1 = Label(self, text="Width")
            label1.pack(side=TOP, pady=(6, 0))

            self.circle_width = Scale(self, from_=5.0, to=1.0, resolution=0.1, sliderlength=25,
                                      command=self.set_circle_width)
            self.circle_width.set(settings["CIRCLE_WIDTH"])
            self.circle_width.pack(side=TOP)

        def set_circle_width(self, event):
            settings["CIRCLE_WIDTH"] = self.circle_width.get()
