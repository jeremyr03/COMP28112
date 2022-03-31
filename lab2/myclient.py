import sys
import tkinter
from tkinter import ttk, scrolledtext, messagebox

from ex2utils import Client
from tkinter import *


class IRCClient(Client):

    def __init__(self):
        super(IRCClient, self).__init__()

    def onMessage(self, socket, message):
        global g
        # *** process incoming messages here ***
        print(message)
        message += '\n\n'
        g.chatBox["state"] = NORMAL
        g.chatBox.insert(END, message)
        g.chatBox["state"] = DISABLED
        return True


def goodbye():
    global g, client
    tkinter.messagebox.showinfo("Closing", "Goodbye. Thank you for using this service")
    g.root.destroy()
    client.stop()


class GUI:

    def __init__(self):
        self.text = None
        self.sendMessage = None
        self.chatBox = None
        self.client = None
        self.ip = None
        self.port = None
        self.scrollableFrame = None
        self.scrollbar = None
        self.canvas = None
        self.container = None
        self.name = None
        # self.setClient()
        self.root = Tk()
        # self.root.geometry('800x600')
        self.root.title("Messaging System for Healthcare Professionals")
        self.setClient()

    def setClient(self):
        global client
        # Parse the IP address and port you wish to connect to.
        self.ip = sys.argv[1]
        self.port = int(sys.argv[2])

        # Create an IRC client.
        client = IRCClient()

        # Start server
        client.start(self.ip, self.port)

    def setUp(self):
        self.chatBox = scrolledtext.ScrolledText(self.root, height=30, width=90)
        self.chatBox.grid(column=1, columnspan=5, row=1, padx=10, pady=10, sticky=N + S + E + W)
        self.chatBox["state"] = NORMAL
        self.chatBox.insert(END, "Messaging System for Healthcare Professionals\n\n")
        self.chatBox["state"] = DISABLED
        self.text = Text(self.root, height=2, width=1)
        self.text.grid(column=1, row=2, columnspan=4, sticky=N + S + E + W)
        self.sendMessage = Button(self.root, text="Send", command=self.send)
        self.sendMessage.grid(column=5, row=2, sticky=N + S + E + W)
        self.root.bind("<Return>", self.send)
        self.root.protocol("WM_DELETE_WINDOW", goodbye)
        self.root.mainloop()

    def send(self, e=None):
        print("works")
        global client
        inp = self.text.get("1.0", tkinter.END + "-1c")

        print(inp)
        # self.chatBox.configure(state='normal')
        if inp.upper().strip() == "CLOSE":
            goodbye()
        else:
            client.send(inp.encode())
            inp += '\n'
            self.chatBox["state"] = NORMAL
            self.chatBox.insert(END, inp)
            self.chatBox["state"] = DISABLED
            self.text.delete('1.0', END)


client = None
g = GUI()
g.setUp()
