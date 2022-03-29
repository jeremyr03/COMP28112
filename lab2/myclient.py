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
        g.chatBox.configure(state='normal')
        g.chatBox.insert(tkinter.INSERT, message)
        g.chatBox.configure(state='disabled')
        return True

    def onDisconnect(self, socket):
        print("d")

    def onStop(self):
        print("S")


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
        self.chatBox.configure(state="normal")
        self.chatBox.insert(tkinter.INSERT, "Messaging System for Healthcare Professionals\n\n")
        self.chatBox.configure(state="disabled")
        self.text = Text(self.root, height=1, width=1)
        self.text.grid(column=1, row=2, columnspan=4, sticky=N + S + E + W)
        self.sendMessage = Button(self.root, text="Send", command=self.send)
        self.sendMessage.grid(column=5, row=2, sticky=N + S + E + W)
        self.root.bind("<Return>", self.send)
        self.root.protocol("WM_DELETE_WINDOW", self.goodbye)
        self.root.mainloop()

    def send(self, e=None):
        print("works")
        global client
        inp = self.text.get("1.0", "end-1c")

        print(inp)
        self.chatBox.configure(state='normal')
        if inp.upper().strip() == "CLOSE":
            self.goodbye()
        else:
            client.send(inp.encode())
            inp += '\n'
            self.chatBox.configure(state='normal')
            self.chatBox.insert(tkinter.INSERT, inp)
            self.chatBox.configure(state='disabled')
            self.text.delete('1.0', END)

    def goodbye(self):
        global client
        tkinter.messagebox.showinfo("Closing", "Goodbye. Thank you for using this service")
        client.stop()
        self.root.destroy()


client = None
g = GUI()
g.setUp()
