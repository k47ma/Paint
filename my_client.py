import threading
import socket
import tkMessageBox
from tkinter import *
from config import settings

# module for client side program


class ClientSettingWindow(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.parent = parent
        self.wm_geometry("300x150")
        self.title("Server Setting")
        self.iconbitmap(r'image\paint.ico')
        self.resizable(False, False)

        container = Frame(self)
        container.pack(side=TOP, padx=6, pady=6, fill=BOTH, expand=True)

        lbl1 = Label(container, text="Host: ")
        lbl1.grid(row=0, column=0, padx=10, pady=5, sticky=E)

        lbl2 = Label(container, text="Port Number: ")
        lbl2.grid(row=1, column=0, padx=10, pady=5, sticky=E)

        self.host_name = Entry(container)
        self.host_name.grid(row=0, column=1, sticky=E+W)
        self.host_name.bind("<Return>", self.create_connection)

        self.port_number = Entry(container)
        self.port_number.grid(row=1, column=1, sticky=E+W)
        self.port_number.bind("<Return>", self.create_connection)

        self.status = Label(self, font=("", 9), fg="red")
        self.status.pack(side=TOP)

        self.connect_btn = Button(self, text="Create", command=self.create_connection)
        self.connect_btn.pack(side=BOTTOM, ipadx=3, ipady=1, pady=(3, 6))

    def create_connection(self, event=None):
        self.status["text"] = ""

        host = self.host_name.get()
        settings["HOST"] = host

        try:
            port = int(self.port_number.get())
            settings["PORT"] = port
        except ValueError:
            tkMessageBox.showinfo("Error", "Please input a valid port number!")
            return

        if not port:
            tkMessageBox.showinfo("Error", "Please input a valid port number!")
            return

        try:
            s = socket.socket()
            host = settings["HOST"]
            port = settings["PORT"]
            s.connect((host, port))

            thread = ClientThread(s)
            thread.daemon = True
            thread.start()

            self.destroy()

            controller = settings["CONTROLLER"]
            controller.status.configure(text="Connected to:\n" + host + " - " + str(port), fg="#228B22")
        except Exception:
            self.status["text"] = "Can't connect to the given host at given port.\nPlease check your input!"


# thread for new client connection
class ClientThread(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)

    def run(self):
        pass
