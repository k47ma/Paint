from Canvas import *
from Controller import *


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


paint = Paint()
paint.mainloop()
