import sys
import im
import time
import urllib.error


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
        # self.user = None
        self.message = ''
        try:
            self.server = im.IMServerProxy('https://web.cs.manchester.ac.uk/t11915jr/COMP28112/lab1/IMserver.php')
        except urllib.error:
            print("Cannot connect to server :( \nAre you connected to Eduroam/GlobalConnect VPN???")
            sys.exit(1)

    def connect(self):
        # server['conn'] is used to let the clients know what is happening:
        # 0 = no one connected; 1 = one person connected; connected = connection established, start mesaging service
        # closing = server is being shut down
        try:
            if len(self.server.keys()) == 1:
                self.server['conn'] = '0'
            elif decode(self.server['conn']) == 'closing':
                self.server.clear()
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
                    self.close_connection("timeout. Second user not found. Closing connection to server.")
                time.sleep(1)

            print(f'connected. Welcome to the Messaging System for Healthcare Professionals.\n')
            print('-------------------------------------------------------\n')
            # server['received'] used to determine whether the other user has received the message or not
            self.server['received'] = encode('0')
            # server['message'] sends the message to the other user
            self.server['message'] = encode('')

        # if ctrl+c is used to stop the execution of the program
        except KeyboardInterrupt:
            self.close_connection("Connection interrupted by keyboard. Closing connection to server", 1)
        except urllib.error.URLError or urllib.error.HTTPError:
            print("Cannot connect to server :( \nAre you connected to Eduroam/GlobalConnect VPN???")
            sys.exit(1)

    def start_im_service(self):
        try:
            while self.check_connection():
                # self.turn used to decide whether to listen for message or to receive message
                if self.turn:
                    self.send_message()
                else:
                    self.await_message()
            self.close_connection("Other user left the conversation. " +
                                  "Thank you for using the Messaging System for Healthcare Professionals.")
        # if ctrl+c is used to stop the execution of the program
        except KeyboardInterrupt:
            self.close_connection("Connection interrupted by keyboard. Closing connection to server", 1)

    def send_message(self):
        myMessage = input("Enter a message to send to the other user: ")

        if self.check_connection():
            # message validation
            if myMessage == '\n' or myMessage == '':
                print(f'{colours.FAIL}Error. No message to send...{colours.ENDC}')
                # by returning nothing, it will end the function which is then called again in start_im_service(),
                # to then ask for the message again
                return
            self.server['message'] = encode(myMessage)
            loading = ""
            # to ensure other user has received the message before then listening for a message
            while decode(self.server['received']) == '0':
                print(f"message sending{loading}", end='\r')
                if loading.count('.') >= 10:
                    self.close_connection("timeout. Message could not be sent")
                time.sleep(1)
                loading += '.'
            print("\nmessage sent")
            self.server['received'] = encode('0')
            self.next_turn()
        else:
            self.close_connection("Connection with user ended. Closing connection to server.")

    def await_message(self):
        timeout = 0
        while decode(self.server['message']) == '':
            if self.check_connection():
                print("Other user is typing", end='\r')
                time.sleep(1)
                timeout += 1
                if timeout == 15:
                    self.close_connection("Other user took too long to send a message. Connection to server is ended")

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
            self.server['conn'] = encode('0')
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
