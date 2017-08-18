import threading
import socket
import tkMessageBox
import random
import os
import re
from PIL import ImageGrab
from tkinter import *
from config import settings
from ast import literal_eval

# module for server side program


class ServerSettingWindow(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.parent = parent
        self.wm_geometry("250x120+%d+%d" % (self.parent.winfo_rootx() + 50, self.parent.winfo_rooty() + 50))
        self.title("Server Setting")
        self.iconbitmap(r'image\paint.ico')
        self.resizable(False, False)

        host = socket.gethostbyname(socket.gethostname())
        settings["HOST"] = host

        container = Frame(self)
        container.pack(side=TOP, padx=6, pady=6, fill=BOTH, expand=True)

        lbl1 = Label(container, text="Host: ")
        lbl1.grid(row=0, column=0, padx=10, pady=5, sticky=E)

        lbl2 = Label(container, text="Port Number: ")
        lbl2.grid(row=1, column=0, padx=10, pady=5, sticky=E)

        host_name = Label(container, text=host)
        host_name.grid(row=0, column=1, sticky=W)

        self.port_number = Entry(container)
        self.port_number.grid(row=1, column=1, sticky=E+W)
        self.port_number.bind("<Return>", self.create_server)

        self.connect_btn = Button(self, text="Create", command=self.create_server)
        self.connect_btn.pack(side=BOTTOM, ipadx=3, ipady=1, pady=(3, 6))

    def create_server(self, event=None):
        try:
            port = int(self.port_number.get())
        except ValueError:
            tkMessageBox.showinfo("Error", "Please input a valid port number!", parent=self)
            return

        if not port:
            tkMessageBox.showinfo("Error", "Please input a valid port number!", parent=self)
            return

        settings["PORT"] = port
        thread = ServerThread()
        thread.daemon = True
        thread.start()
        self.destroy()


# thread for new server
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.s = socket.socket()
        host = settings["HOST"]
        port = settings["PORT"]
        self.s.bind((host, port))
        self.s.listen(3)

        controller = settings["CONTROLLER"]
        controller.status.configure(text="Waiting for connection...\n" + host + " - " + str(port), fg="#6495ED")

    def run(self):
        # waiting for client to connect
        while True:
            client, addr = self.s.accept()
            self.set_status(addr)
            settings["SOCKET"] = client

            # set up receiving thread
            thread = ServerReceivingThread(client)
            thread.daemon = True
            thread.start()

            # send current paint to the client
            self.send_image(client)

    def set_status(self, addr):
        controller = settings["CONTROLLER"]
        controller.status.configure(text="Connected from:\n" + addr[0] + " - " + str(addr[1]), fg="#228B22")

    def send_image(self, client):
        # fetch the current canvas coordsition
        canvas = settings["CANVAS"]
        x1 = canvas.parent.winfo_rootx() + canvas.winfo_x()
        y1 = canvas.parent.winfo_rooty() + canvas.winfo_y()
        x2 = x1 + canvas.winfo_width()
        y2 = y1 + canvas.winfo_height()

        # generate a random file name and save it to gif file
        fname = "documents\\" + hex(random.randint(10e20, 10e21))[2:][:-1] + ".gif"
        ImageGrab.grab().crop((x1, y1, x2, y2)).save(fname)

        # send file size to the client
        fsize = os.path.getsize(fname)
        client.send(str(fsize))

        # send the image to the client
        image = open(fname, 'rb')
        while True:
            string = image.read(512)
            if not string:
                break
            client.send(string)

        # clean up the gif image
        image.close()
        os.remove(fname)


# listen to the client
class ServerReceivingThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)

        self.client = client
        self.last_draw = None

    def run(self):
        try:
            while True:
                datas = self.client.recv(1024)
                for data in re.findall("{.*?}", datas):
                    try:
                        data = literal_eval(data)
                    except ValueError:
                        continue
                    except TypeError:
                        continue
                    except SyntaxError:
                        continue

                    canvas = settings["CANVAS"]

                    if data["type"] == "mouse":
                        # update mouse coordsition
                        coords = data["data"]
                        cursor = PhotoImage(file="image\\cursor2.gif")
                        canvas.create_image(coords, image=cursor, anchor=NW)
                    elif data["type"] == "pencil":
                        # add pencil line
                        coords, color, width = data["data"]
                        canvas.create_line(coords, fill=color, width=width, capstyle=ROUND, joinstyle=ROUND)
                    elif data["type"] == "brush":
                        # add brush line
                        type, coords, color, width = data["data"]
                        if type == "circle":
                            canvas.create_line(coords, fill=color, width=width, capstyle=ROUND, joinstyle=ROUND)
                        else:
                            canvas.create_line(coords, fill=color, width=width, capstyle=PROJECTING, joinstyle=BEVEL)
                    elif data["type"] == "text":
                        # add text
                        x, y, text, font, width, text_color = data["data"]
                        canvas.create_text(x, y, text=text, anchor=NW, font=font, width=width, fill=text_color)
                    elif data["type"] == "background":
                        # add background for text
                        coords, color, fill_color = data["data"]
                        canvas.create_rectangle(coords, outline=color, fill=fill_color)
                    elif data["type"] == "line":
                        # clear last line
                        if self.last_draw:
                            canvas.delete(self.last_draw)

                        # add new line
                        coords, color, width = data["data"]
                        line = canvas.create_line(coords, fill=color, width=width, capstyle=ROUND)
                        self.last_draw = line
                    elif data["type"] == "set":
                        self.last_draw = None
        except Exception:
            controller = settings["CONTROLLER"]
            host = settings["HOST"]
            port = settings["PORT"]
            controller.status.configure(text="Waiting for connection...\n" + host + " - " + str(port), fg="#6495ED")
