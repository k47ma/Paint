import tkFont
import tkMessageBox
from tkinter import *
from tooltip import *
from config import *
import tkColorChooser


# frame for control buttons
class ControlFrame(Frame):
    def __init__(self, parent, canvas):
        Frame.__init__(self, parent, width=130)

        self.pack_propagate(False)
        self.canvas = canvas
        self.canvas.controller = self
        self.types = {}
        self.cursors = {}

        # tools setting
        tools_frame = LabelFrame(self, text="Tools")
        tools_frame.pack(side=TOP, fill=BOTH, pady=(6, 0), ipady=5)

        tools_btn_frame = Frame(tools_frame)
        tools_btn_frame.pack(side=TOP)

        self.pencil_img = PhotoImage(file="image\\pencil.gif")
        pencil_btn = Button(tools_btn_frame, image=self.pencil_img, cursor="hand2", command=lambda: self.select("pencil"))
        pencil_btn.grid(row=0, column=0)
        self.create_tooltip(pencil_btn, "pencil")
        self.types["pencil"] = pencil_btn
        self.cursors["pencil"] = "@pencil.cur"

        self.brush_img = PhotoImage(file="image\\brush.gif")
        brush_btn = Button(tools_btn_frame, image=self.brush_img, cursor="hand2", command=lambda: self.select("brush"))
        brush_btn.grid(row=1, column=0)
        self.create_tooltip(brush_btn, "brush")
        self.types["brush"] = brush_btn
        self.cursors["brush"] = "@brush.cur"

        self.eraser_img = PhotoImage(file="image\\eraser.gif")
        eraser_btn = Button(tools_btn_frame, image=self.eraser_img, cursor="hand2", command=lambda: self.select("eraser"))
        eraser_btn.grid(row=2, column=0)
        self.create_tooltip(eraser_btn, "eraser")
        self.types["eraser"] = eraser_btn
        self.cursors["eraser"] = "@eraser.cur"

        self.text_img = PhotoImage(file="image\\text.gif")
        text_btn = Button(tools_btn_frame, image=self.text_img, cursor="hand2", command=lambda: self.select("text"))
        text_btn.grid(row=3, column=0)
        self.create_tooltip(text_btn, "textfield")
        self.types["text"] = text_btn
        self.cursors["text"] = "tcross"

        self.line_img = PhotoImage(file="image\\line.gif")
        line_btn = Button(tools_btn_frame, image=self.line_img, cursor="hand2", command=lambda: self.select("line"))
        line_btn.grid(row=0, column=1)
        self.create_tooltip(line_btn, "line")
        self.types["line"] = line_btn
        self.cursors["line"] = "plus"

        self.rect_img = PhotoImage(file="image\\rect.gif")
        rect_btn = Button(tools_btn_frame, image=self.rect_img, cursor="hand2", command=lambda: self.select("rect"))
        rect_btn.grid(row=1, column=1)
        self.create_tooltip(rect_btn, "rectangle")
        self.types["rect"] = rect_btn
        self.cursors["rect"] = "tcross"

        self.oval_img = PhotoImage(file="image\\oval.gif")
        circle_btn = Button(tools_btn_frame, image=self.oval_img, cursor="hand2", command=lambda: self.select("circle"))
        circle_btn.grid(row=2, column=1)
        self.create_tooltip(circle_btn, "oval")
        self.types["circle"] = circle_btn
        self.cursors["circle"] = "tcross"

        self.revert_img = PhotoImage(file="image\\revert.gif")
        revert_btn = Button(tools_btn_frame, image=self.revert_img, cursor="hand2", command=self.canvas.revert)
        revert_btn.grid(row=4, column=0, pady=3)
        self.create_tooltip(revert_btn, "revert")

        # colors setting
        color_frame = LabelFrame(self, text="Colors")
        color_frame.pack(side=TOP, fill=BOTH, pady=(6, 0), ipady=5)
        color_frame.columnconfigure(0, weight=1)
        color_frame.columnconfigure(1, weight=2)
        color_frame.columnconfigure(2, weight=2)

        color_label = Label(color_frame, text="Outline", anchor=CENTER)
        color_label.grid(row=0, column=0)

        color_btn_frame = Frame(color_frame, width=25, height=25)
        color_btn_frame.pack_propagate(False)
        color_btn_frame.grid(row=1, column=0)

        self.color_btn = Button(color_btn_frame, bg=settings["COLOR"], bd=2, relief=GROOVE,
                                activebackground=settings["COLOR"], command=self.select_color)
        self.color_btn.pack(side=TOP, fill=BOTH, expand=True)

        fill_color_label = Label(color_frame, text="Fill", anchor=CENTER)
        fill_color_label.grid(row=0, column=1)

        fill_color_btn_frame = Frame(color_frame, width=25, height=25)
        fill_color_btn_frame.pack_propagate(False)
        fill_color_btn_frame.grid(row=1, column=1)

        self.fill_color_btn = Button(fill_color_btn_frame, bg=settings["FILL_COLOR"], bd=2, relief=GROOVE,
                                     activebackground=settings["FILL_COLOR"], command=self.select_fill_color)
        self.fill_color_btn.pack(side=TOP, fill=BOTH, expand=True)

        font_color_lbl = Label(color_frame, text="Text")
        font_color_lbl.grid(row=0, column=2)

        font_color_frame = Frame(color_frame, width=25, height=25)
        font_color_frame.pack_propagate(False)
        font_color_frame.grid(row=1, column=2)

        self.color_btn = Button(font_color_frame, bg=settings["TEXT_COLOR"], bd=2, relief=GROOVE,
                                activebackground=settings["TEXT_COLOR"], command=self.select_text_color)
        self.color_btn.pack(side=TOP, fill=BOTH, expand=True)

        self.transparency_var = IntVar()
        self.transparency_var.set(1)
        self.transparency = Checkbutton(color_frame, text="Transparent Fill", variable=self.transparency_var,
                                        command=self.set_transparency)
        self.transparency.grid(row=2, column=0, columnspan=3, pady=(5, 0))

        self.clear_img = PhotoImage(file="image\\cross.gif")
        clear_btn = Button(self, image=self.clear_img, cursor="hand2", command=self.ask_clear)
        clear_btn.pack(side=BOTTOM, pady=10)
        self.create_tooltip(clear_btn, "clear all")

        self.position = Label(self, text="(0, 0)", font=("Arial", 8))
        self.position.pack(side=BOTTOM)

        # settings for specific tool
        self.setting_frame = SettingFrame(self)
        self.setting_frame.pack(side=TOP, fill=BOTH, expand=True, ipady=6, pady=6)

        self.select("pencil")
        self.setting_frame.show("pencil")

    def printMousePosition(self, event):
        self.position["text"] = "(%d, %d)" % (event.x, event.y)

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

    def select_text_color(self):
        selected_color = tkColorChooser.askcolor(settings["TEXT_COLOR"], parent=self.parent,
                                                 title="Select Outline Color")
        if selected_color[1]:
            settings["TEXT_COLOR"] = selected_color[1]
            self.color_btn["bg"] = settings["TEXT_COLOR"]

    def set_transparency(self):
        settings["TRANSPARENT"] = bool(self.transparency_var.get())

    def create_tooltip(self, widget, text):
        Tooltip(widget, text)

    def ask_clear(self):
        clear = tkMessageBox.askyesno("Clear Canvas", "Are you sure you want to clear the canvas?", default="no")
        if clear:
            self.canvas.clear()


# frame for containing tool settings
class SettingFrame(LabelFrame):
    def __init__(self, parent):
        LabelFrame.__init__(self, parent, text="Settings")

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

        text_frame = self.TextFrame(self)
        text_frame.grid(row=0, column=0, sticky=NSEW)
        self.frames["text"] = text_frame

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

            shape_frame = Frame(self)
            shape_frame.pack(side=TOP)

            shape_circle = Label(shape_frame, text=u"\u26ab", font=("times", 10), anchor=W)
            shape_circle.grid(row=0, column=1)

            shape_rect = Label(shape_frame, text=u"\u25a0", font=("times", 15), anchor=W)
            shape_rect.grid(row=1, column=1)

            self.mode = StringVar()
            self.mode.set("circle")

            mode1 = Radiobutton(shape_frame, variable=self.mode, value="circle", command=self.set_brush_mode)
            mode2 = Radiobutton(shape_frame, variable=self.mode, value="square", command=self.set_brush_mode)
            mode1.grid(row=0, column=0)
            mode2.grid(row=1, column=0)

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

            shape_frame = Frame(self)
            shape_frame.pack(side=TOP)

            shape_circle = Label(shape_frame, text=u"\u26ab", font=("times", 10), anchor=W)
            shape_circle.grid(row=0, column=1)

            shape_rect = Label(shape_frame, text=u"\u25a0", font=("times", 15), anchor=W)
            shape_rect.grid(row=1, column=1)

            self.mode = StringVar()
            self.mode.set("circle")

            mode1 = Radiobutton(shape_frame, variable=self.mode, value="circle", command=self.set_eraser_mode)
            mode2 = Radiobutton(shape_frame, variable=self.mode, value="square", command=self.set_eraser_mode)
            mode1.grid(row=0, column=0)
            mode2.grid(row=1, column=0)

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

    class TextFrame(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)
            self.parent = parent

            # font family setting
            font_family_frame = Frame(self)
            font_family_frame.pack(side=TOP, pady=(3, 0), padx=5)

            font_families = sorted(tkFont.families())

            font_family_label = Label(font_family_frame, text="Font Family")
            font_family_label.pack(side=TOP)

            font_family = Listbox(font_family_frame, height=1)
            font_family.pack(side=TOP)

            for font in font_families:
                font_family.insert(END, font)

            # font size setting
            font_size_frame = Frame(self)
            font_size_frame.pack(side=TOP, pady=(6, 0), padx=5)

            font_size_label = Label(font_size_frame, text="Font Size")
            font_size_label.pack(side=TOP)

            font_size_var = IntVar()
            font_size_var.set(10)
            font_size = Spinbox(font_size_frame, textvariable=font_size_var, from_=0, to=100)
            font_size.pack(side=TOP)

            # font decoration setting
            decoration_frame = Frame(self)
            decoration_frame.pack(side=TOP, pady=(6, 0))

            weight_btn = Button(decoration_frame, text="T", font=("times", 10, "bold"))
            weight_btn.grid(row=0, column=0)

            slant_btn = Button(decoration_frame, text="T", font=("times", 10, "italic"))
            slant_btn.grid(row=0, column=1)

            underline_btn = Button(decoration_frame, text="T", font=("times", 10, "underline"))
            underline_btn.grid(row=0, column=2)

            overstrike_btn = Button(decoration_frame, text="T", font=("times", 10, "overstrike"))
            overstrike_btn.grid(row=0, column=3)
