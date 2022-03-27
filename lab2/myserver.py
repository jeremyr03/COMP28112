import sys
from ex2utils import Server


class colours:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MyServer(Server):

    def __init__(self):
        super(MyServer, self).__init__()
        self.users = {}
        self.userCount = len(self.users)

    def onStart(self):
        print("Server has started")

    def onStop(self):
        print("server ended")

    def onConnect(self, socket):
        self.userCount += 1
        print(f"user connected, Current number of users: {self.userCount}")

    def signedIn(self):
        return

    def onMessage(self, socket, message):
        (command, sep, parameter) = message.strip().partition(' ')
        print(f"command: {colours.GREEN}{command}{colours.NORMAL}")
        print(f"Message: {colours.BLUE}{parameter}{colours.NORMAL}")

        if command.upper() == "HELP" and parameter == '':
            toSend = "\n Welcome to Jeremy's server. \n\nCommands:\n" \
                     f"{colours.GREEN}SET_NAME <username>{colours.NORMAL} - sets a username for user " \
                     f"{colours.WARNING}(N.B. Username must not contain spaces){colours.NORMAL}\n" \
                     f"{colours.GREEN}MESSAGE <message>{colours.NORMAL} - sends a message to all users\n" \
                     f"{colours.GREEN}DM <user> <message>{colours.NORMAL} - sends a message to a specific user\n\n" \
                     f"{colours.WARNING}Note: A username is required to send messages{colours.NORMAL}\n\n"
            socket.send(toSend.encode())

        elif parameter == '':
            toSend = "Invalid command. Try again and ensure it is in the format".encode() + \
                     f" {colours.WARNING}<COMMAND> <PARAMETER[S]>{colours.NORMAL} ".encode() + \
                     f"{colours.BOLD} separated by spaces{colours.NORMAL}".encode()
            socket.send(toSend)

        elif command.upper() == "SET_NAME":
            if parameter.count(' ') > 0:
                toSend = f"{colours.WARNING}Spaces are not allowed in username{colours.NORMAL}".encode()
                socket.send(toSend)
            elif self.users.get(parameter) is not None:
                if self.users.get(parameter) == socket:
                    toSend = f"{colours.WARNING}Username already set to {parameter}{colours.NORMAL}".encode()
                    socket.send(toSend)
                else:
                    toSend = f"{colours.WARNING}user already exists{colours.NORMAL}".encode()
                    socket.send(toSend)
            else:
                if socket in list(self.users.values()):
                    oldUsername = list(self.users.keys())[list(self.users.values()).index(socket)]
                    self.users.pop(oldUsername)
                    toSend = f"{colours.HEADER}username changed to: {colours.BLUE}{parameter}{colours.NORMAL}"
                else:
                    toSend = f"{colours.HEADER}username set: {colours.BLUE}{parameter}{colours.NORMAL}"
                print(toSend)
                self.users[parameter] = socket
                socket.send(toSend.encode())

        elif command.upper() == "MESSAGE":
            if socket in self.users.values():
                if self.userCount != 1:
                    for key, val in self.users.items():
                        if val != socket:
                            toSend = f"Message from " \
                                     f"{colours.BLUE}" \
                                     f"{list(self.users.keys())[list(self.users.values()).index(socket)]}" \
                                     f"{colours.NORMAL}: {colours.GREEN}{parameter}{colours.NORMAL}"

                        else:
                            toSend = f"You sent:{colours.GREEN}{parameter}{colours.NORMAL}"
                        val.send(toSend.encode())

                else:
                    toSend = f"{colours.WARNING}There are no other users to send your message to.{colours.NORMAL}"
                    socket.send(toSend.encode())
            else:
                toSend = f"{colours.WARNING}Assign yourself a username to be able to send a message.{colours.NORMAL}"
                socket.send(toSend.encode())

        elif command.upper() == "DM":
            if socket in self.users.values():
                (DM, sep, msg) = parameter.strip().partition(' ')

                if DM in self.users.keys():
                    receiver = self.users[DM]
                    if receiver != list(self.users.keys())[list(self.users.values()).index(socket)]:
                        toSend2 = f"Message from " \
                                 f"{colours.BLUE}{list(self.users.keys())[list(self.users.values()).index(socket)]}" \
                                 f"{colours.NORMAL}: {colours.GREEN}{parameter}{colours.NORMAL}"
                        toSend = f"You sent:{colours.GREEN}{parameter}{colours.NORMAL}"
                        receiver.send(toSend2.encode())
                    else:
                        toSend = f"{colours.WARNING}You can't DM yourself!!!{colours.NORMAL}"
                else:
                    toSend = f"{colours.WARNING}User could not be found.{colours.NORMAL}"
            else:
                toSend = f"{colours.WARNING}Assign yourself a username to be able to send a message.{colours.NORMAL}"
            socket.send(toSend.encode())

        else:
            print("Unkown command")
            toSend = "Invalid command. Try again and ensure it is in the format".encode() + \
                     f" {colours.WARNING}<COMMAND> <PARAMETER[S]>{colours.NORMAL} ".encode() + \
                     f"{colours.BOLD} separated by spaces{colours.NORMAL}".encode()
            socket.send(toSend)


        return True

    def onDisconnect(self, socket):
        # self.users.pop(list(self.users.keys())[list(self.users.values()).index(socket)])
        self.userCount -= 1
        print(f"disconnecting user. Current number of users: {self.userCount}")


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()
server.start(ip, port)
