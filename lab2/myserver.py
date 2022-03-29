import sys
import time

from ex2utils import Server


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

    def onMessage(self, socket, message):
        (command, sep, parameter) = message.strip().partition(' ')
        print(f"command: {command}")
        print(f"Message: {parameter}")

        if command == '' and parameter == '':
            pass
        elif command.upper() == "HELP" and parameter == '':
            toSend = "\n Messaging System for Health-care Professionals \nCommands:\n" \
                     "SET_NAME <username> - sets a username for user " \
                     "(N.B. Username must not contain spaces)\n" \
                     "MESSAGE <message> - sends a message to all users\n" \
                     "DM <user> <message> - sends a message to a specific user\n" \
                     "CLOSE - terminate connection to server\n" \
                     "HELP - provides a list of commands\n" \
                     "Note: A username is required to send messages\n\n"
            socket.send(toSend.encode())

        elif command.upper() == "CLOSE" and parameter == '':
            toSend = "Thank you for using this service"
            socket.send(toSend.encode())

        elif parameter == '':
            toSend = "Invalid command. Try again and ensure it is in the format".encode() + \
                     " <COMMAND> <PARAMETER[S]> ".encode() + \
                     " separated by spaces}".encode()
            socket.send(toSend)

        elif command.upper() == "SET_NAME":
            parameter = parameter.upper()
            if parameter.count(' ') > 0:
                toSend = "Spaces are not allowed in username".encode()
                socket.send(toSend)
            elif self.users.get(parameter) is not None:
                if self.users.get(parameter) == socket:
                    toSend = f"Username already set to {parameter}".encode()
                    socket.send(toSend)
                else:
                    toSend = f"user already exists".encode()
                    socket.send(toSend)
            else:
                if socket in list(self.users.values()):
                    oldUsername = list(self.users.keys())[list(self.users.values()).index(socket)]
                    self.users.pop(oldUsername)
                    toSend = f"username changed to: {parameter}"
                else:
                    toSend = f"username set: {parameter}"
                print(toSend)
                self.users[parameter] = socket
                socket.send(toSend.encode())

        elif command.upper() == "MESSAGE":
            if socket in self.users.values():
                if self.userCount != 1:
                    for key, val in self.users.items():
                        if val != socket:
                            toSend = f"Message from " +\
                                     f"{list(self.users.keys())[list(self.users.values()).index(socket)]}" +\
                                     f": {parameter}"
                            val.send(toSend.encode())

                else:
                    toSend = f"There are no other users to send your message to."
                    socket.send(toSend.encode())
            else:
                toSend = f"Assign yourself a username to be able to send a message."
                socket.send(toSend.encode())

        elif command.upper() == "DM":
            if socket in self.users.values():
                (DM, sep, msg) = parameter.strip().partition(' ')
                DM = DM.upper()
                if DM in self.users.keys():
                    receiver = self.users[DM]
                    if receiver != socket:
                        toSend = f"Message from " +\
                                 f"{list(self.users.keys())[list(self.users.values()).index(socket)]}" +\
                                 f": {msg}"
                        receiver.send(toSend.encode())
                    else:
                        toSend = "You can't DM yourself!!!"
                        socket.send(toSend.encode())
                else:
                    toSend = f"User could not be found."
                    socket.send(toSend.encode())
            else:
                toSend = f"Assign yourself a username to be able to send a message."
                socket.send(toSend.encode())

        else:
            print("Unknown command")
            toSend = "Invalid command. Try again and ensure it is in the format".encode() + \
                     " <COMMAND> <PARAMETER[S]>".encode() + \
                     " separated by spaces".encode()
            socket.send(toSend)

        return True

    def onDisconnect(self, socket):
        if socket in self.users.values():
            self.users.pop(list(self.users.keys())[list(self.users.values()).index(socket)])
        self.userCount -= 1
        print(f"disconnecting user. Current number of users: {self.userCount}")


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()
server.start(ip, port)
