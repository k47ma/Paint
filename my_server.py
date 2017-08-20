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
        self.history = []
        self.bitmaps = []

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
                            # update mouse position
                            pos = data["data"]
                            cursor = PhotoImage(file="image\\cursor2.gif")
                            canvas.create_image(pos, image=cursor, anchor=NW)
                        elif data["type"] == "pencil":
                            if not self.last_draw:
                                self.last_draw = []
                            # add pencil line
                            pos, color, width = data["data"]
                            line = canvas.create_line(pos, fill=color, width=width, capstyle=ROUND, joinstyle=ROUND)
                            self.last_draw.append(line)
                            self.history.append(line)
                        elif data["type"] == "brush":
                            if not self.last_draw:
                                self.last_draw = []
                            # add brush line
                            brush_type, pos, color, width = data["data"]
                            if brush_type == "circle":
                                brush = canvas.create_line(pos, fill=color, width=width, capstyle=ROUND,
                                                           joinstyle=ROUND)
                            else:
                                brush = canvas.create_line(pos, fill=color, width=width, capstyle=PROJECTING,
                                                           joinstyle=BEVEL)
                            self.last_draw.append(brush)
                            self.history.append(brush)
                        elif data["type"] == "textarea":
                            text_data = data["data"]["text"]
                            background_data = data["data"]["background"]
                            action = []
                            if background_data:
                                # add background for text
                                coords, color, fill_color = background_data
                                background = canvas.create_rectangle(coords, outline=color, fill=fill_color)
                                action.append(background)
                            # add text
                            x, y, text, font, width, text_color = text_data
                            text = canvas.create_text(x, y, text=text, anchor=NW, font=font, width=width,
                                                      fill=text_color)
                            action.append(text)
                            self.history.append(action)
                        elif data["type"] == "line":
                            # clear last line
                            if self.last_draw:
                                canvas.delete(self.last_draw)
                            # add new line
                            coords, color, width = data["data"]
                            line = canvas.create_line(coords, fill=color, width=width, capstyle=ROUND)
                            self.last_draw = line
                        elif data["type"] == "set":
                            if self.last_draw:
                                self.history.append(self.last_draw)
                            self.last_draw = None
                        elif data["type"] == "rect":
                            # clear last rectangle
                            if self.last_draw:
                                canvas.delete(self.last_draw)
                            # add new rectangle
                            coords, width, color, fill_color = data["data"]
                            rect = canvas.create_rectangle(coords, width=width, outline=color, fill=fill_color)
                            self.last_draw = rect
                        elif data["type"] == "circle":
                            # clear last circle
                            if self.last_draw:
                                canvas.delete(self.last_draw)
                            # add new circle
                            coords, width, color, fill_color = data["data"]
                            circle = canvas.create_oval(coords, width=width, outline=color, fill=fill_color)
                            self.last_draw = circle
                        elif data["type"] == "spray":
                            if not self.last_draw:
                                self.last_draw = []
                            # add spray
                            coords, spray_size = data["data"]
                            image = PhotoImage(file="image\\shaped_spray.gif")
                            zoomed_image = image.zoom(spray_size)
                            self.bitmaps.append(zoomed_image)
                            spray = canvas.create_image(coords, image=self.bitmaps[-1])
                            self.last_draw.append(spray)
                        elif data["type"] == "revert":
                            # get the last action
                            try:
                                last_action = self.history.pop()
                            except IndexError:
                                continue
                            # delete last action from canvas
                            if type(last_action) is int:
                                canvas.delete(last_action)
                            else:
                                for action in last_action:
                                    canvas.delete(action)
        except socket.error:
            controller = settings["CONTROLLER"]
            host = settings["HOST"]
            port = settings["PORT"]
            controller.status.configure(text="Waiting for connection...\n" + host + " - " + str(port), fg="#6495ED")
