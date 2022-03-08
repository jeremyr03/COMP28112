import sys
import im
import time


# problem with server['conn']
class colours:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def decode(m):
    return m.decode().strip()


def encode(m):
    return m.encode('UTF-8')


class Server:

    def __init__(self):
        self.turn = None
        self.user = None
        self.message = ''
        try:
            self.server = im.IMServerProxy('https://web.cs.manchester.ac.uk/t11915jr/COMP28112/lab1/IMserver.php')
        except ConnectionRefusedError:
            print("Cannot connect to server")
            sys.exit(1)

    def connect(self):
        try:
            if len(self.server.keys()) == 1:
                self.server['conn'] = '0'
            if decode(self.server['conn']) == '0':
                self.turn = True
                self.server['conn'] = encode('1')
            elif decode(self.server['conn']) == '1':
                self.turn = False
                self.server['conn'] = encode('connected')
            elif decode(self.server['conn']) == 'connected':
                print("Server is currently in use. Try again later")
                sys.exit()
            else:
                self.close_connection("error with server. Try again")

            loading = ""
            while decode(self.server['conn']) != 'connected':
                print(f"Searching for second user {loading}", end='\r')
                loading += '.'
                if loading.count('.') >= 10:
                    self.close_connection("timeout. Second user not found")
                time.sleep(1)

            print(f'connected. Welcome to the Messaging System for Healthcare Professionals.\n')
            print('-------------------------------------------------------\n')
            self.server['received'] = encode('0')
            self.server['message'] = encode('')

        except KeyboardInterrupt:
            self.close_connection("Connection interrupted by keyboard. Closing connection to server", 1)

    def start_im_service(self):
        try:
            while self.check_connection():
                if self.turn:
                    self.send_message()
                else:
                    self.await_message()
            self.close_connection("Other user left the conversation. " +
                                  "Thank you for using the Messaging System for Healthcare Professionals.")
        except KeyboardInterrupt:
            self.close_connection("Connection interrupted by keyboard. Closing connection to server", 1)

    def send_message(self):
        myMessage = input("Enter a message to send to the other user: ")

        if self.check_connection():
            if myMessage == '\n' or myMessage == '':
                print(f'{colours.WARNING}Error. No message to send...{colours.ENDC}')
                return
            self.server['message'] = encode(myMessage)
            loading = ""
            while decode(self.server['received']) == '0':
                print(f"message sending{loading}", end='\r')
                if loading.count('.') >= 10:
                    self.close_connection("timeout. Message could not be sent")
                time.sleep(1)
                loading += '.'
            print("\nmessage sent")
            self.server['received'] = encode('0')
            self.next_turn()

    def await_message(self):
        while decode(self.server['message']) == '':
            if self.check_connection():
                print("Other user is typing", end='\r')
                time.sleep(1)

        if self.check_connection():
            print("You have received a message:\n" +
                  f"{colours.CYAN}{self.server['message'].decode().strip()}{colours.ENDC}")
            self.server['received'] = encode('1')
            self.server['message'] = encode('')
            self.next_turn()
            time.sleep(1)
        print("\n")

    def next_turn(self):
        self.turn = not self.turn

    def check_connection(self):
        return decode(self.server['conn']) == 'connected'

    def close_connection(self, m='connection to server closed', e=0):
        if decode(self.server['conn']) == 'connected':
            self.server.clear()
            self.server['conn'] = encode('closing')
            print('Closing connection with server')
            sys.exit()

        if decode(self.server['conn']) == 'closing':
            self.server.clear()
            print('Closing connection with server')
            sys.exit()

        else:
            print(m)
            self.server.clear()
            self.server['conn'] = encode('0')
            sys.exit(e)


s = Server()
s.connect()
s.start_im_service()
