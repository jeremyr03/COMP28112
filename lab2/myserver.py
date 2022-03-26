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

    def onStart(self):
        print("Server has started")

    def onStop(self):
        print("server ended")

    def onConnect(self, socket):
        print("user connected")

    def onMessage(self, socket, message):
        print(f"message received: {colours.BLUE}{message}{colours.NORMAL}")
        message = message.upper().encode()
        socket.send(message)
        return True

    def onDisconnect(self, socket):
        print("\ndisconnecting users...")


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()
server.start(ip, port)
