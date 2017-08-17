from canvas import *
from controller import *


# top level class
class Paint(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.iconbitmap(r'image\paint.ico')
        self.wm_title("Paint")
        self.geometry("900x680+0+0")
        self.minsize(900, 640)
        self["cursor"] = "@main.cur"

        canvas_panel = PaintCanvas(self)
        control_frame = ControlFrame(self, canvas_panel)
        control_frame.pack(side=LEFT, fill=Y, expand=False, padx=6, pady=5)
        canvas_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)


if __name__ == '__main__':
    paint = Paint()
    paint.mainloop()
