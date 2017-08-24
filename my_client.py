import threading
import socket
import tkMessageBox
import random
from tkinter import *
from config import settings
from ast import literal_eval


# module for client side program


class ClientSettingWindow(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.parent = parent
        self.wm_geometry("250x160+%d+%d" % (self.parent.winfo_rootx() + 50, self.parent.winfo_rooty() + 50))
        self.title("Client Setting")
        self.iconbitmap(r'image\paint.ico')
        self.resizable(False, False)

        container = Frame(self)
        container.pack(side=TOP, padx=6, pady=(6, 0), fill=BOTH, expand=True)

        lbl1 = Label(container, text="Host: ")
        lbl1.grid(row=0, column=0, padx=10, pady=5, sticky=E)

        lbl2 = Label(container, text="Port Number: ")
        lbl2.grid(row=1, column=0, padx=10, pady=5, sticky=E)

        self.host_name = Entry(container)
        self.host_name.grid(row=0, column=1, sticky=E + W)
        self.host_name.bind("<Return>", self.create_connection)

        self.port_number = Entry(container)
        self.port_number.grid(row=1, column=1, sticky=E + W)
        self.port_number.bind("<Return>", self.create_connection)

        self.status = Label(self, font=("", 9), fg="red")
        self.status.pack(side=TOP)

        self.connect_btn = Button(self, text="Create", command=self.create_connection)
        self.connect_btn.pack(side=BOTTOM, ipadx=3, ipady=1, pady=(3, 6))

    def create_connection(self, event=None):
        host = self.host_name.get()
        if not host:
            self.status["text"] = "Please enter a valid hostname!"
            return

        port = self.port_number.get()
        if not port:
            self.status["text"] = "Please enter a valid port number!"
            return

        try:
            port_number = int(port)
        except ValueError:
            self.status["text"] = "Please enter a valid port number!"
            return

        settings["HOST"] = host
        settings["PORT"] = port_number

        thread = ClientThread(self, host, port_number)
        thread.daemon = True
        thread.start()

    def close_window(self):
        self.destroy()


# thread for new client connection
class ClientThread(threading.Thread):
    def __init__(self, parent, host, port):
        threading.Thread.__init__(self)

        self.parent = parent
        self.host = host
        self.port = port

    def run(self):
        self.parent.status.configure(text="Connecting...", fg="#228B22")

        try:
            self.setup_client()
        except Exception:
            self.parent.status.configure(
                text="Can't connect to the given host at given port.\nPlease check your input!", fg="red")

    def setup_client(self):
        s = socket.socket()
        s.connect((self.host, self.port))
        settings["SOCKET"] = s

        controller = settings["CONTROLLER"]
        controller.status.configure(text="Connected to:\n" + self.host + " - " + str(self.port), fg="#228B22")
        self.parent.status.configure(text="Connected to:\n" + self.host + " - " + str(self.port), fg="#228B22")
        self.parent.connect_btn["state"] = DISABLED

        thread = ClientReceivingThread(s)
        thread.daemon = True
        thread.start()


# thread for listening to messages from server
class ClientReceivingThread(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)

        self.connection = connection
        self.image = None
        self.last_draw = None
        self.history = []
        self.bitmaps = []

    def run(self):
        # get the file size from server
        data = self.connection.recv(1024)
        fsize = int(data)

        # generate a random file name
        fname = "documents\\" + hex(random.randint(10e20, 10e21))[2:][:-1] + ".gif"
        file = open(fname, 'wb')

        # receive image from server
        received_size = 0
        while True:
            data = self.connection.recv(512)
            file.write(data)
            received_size += 512
            if received_size >= fsize:
                break
        file.close()

        # update client canvas
        self.image = PhotoImage(file=fname)
        settings["CANVAS"].create_image((0, 0), image=self.image, anchor=NW)

        # listen to the server
        try:
            while True:
                datas = self.connection.recv(1024)
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
                            brush = canvas.create_line(pos, fill=color, width=width, capstyle=ROUND, joinstyle=ROUND)
                        else:
                            brush = canvas.create_line(pos, fill=color, width=width, capstyle=PROJECTING, joinstyle=BEVEL)
                        self.last_draw.append(brush)
                        self.history.append(brush)
                    elif data["type"] == "textarea":
                        text_data = data["data"][0]
                        background_data = data["data"][1]
                        action = []
                        if background_data:
                            # add background for text
                            coords, color, fill_color = background_data
                            background = canvas.create_rectangle(coords, outline=color, fill=fill_color)
                            action.append(background)
                        # add text
                        x, y, text, font, width, text_color = text_data
                        text = canvas.create_text(x, y, text=text, anchor=NW, font=font, width=width, fill=text_color)
                        action.append(text)
                        self.history.append(action)
                    elif data["type"] == "line":
                        # clear last line
                        if self.last_draw:
                            canvas.delete(self.last_draw)
                        # add new line
                        coords, color, width, dash, dash_width = data["data"]
                        if dash:
                            line = canvas.create_line(coords, fill=color, width=width, capstyle=ROUND,
                                                      dash=(dash_width, ))
                        else:
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
            controller.status.configure(text="Offline", fg="#FF8C00")
