import threading
import socket
import tkMessageBox
from tkinter import *
from config import settings

# module for server side program


class ServerSettingWindow(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.parent = parent
        self.wm_geometry("250x120")
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
            ServerReceivingThread(client)

    def set_status(self, addr):
        controller = settings["CONTROLLER"]
        controller.status.configure(text="Connected from:\n" + addr[0] + " - " + str(addr[1]), fg="#228B22")


# listen to the client
class ServerReceivingThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            message = self.client.recv(1024)
            print message
