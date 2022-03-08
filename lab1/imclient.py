import sys

import im
import time


# problem with server['conn']
class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def end_connection(message="connection to server ended."):
    print(message)
    if len(server.keys()) <= 2:
        print("cleared")
        server.clear()
    else:
        server.clear()
        print("not clear")
        server['conn'] = 'end'
    sys.exit()


try:
    server = im.IMServerProxy('https://web.cs.manchester.ac.uk/t11915jr/COMP28112/lab1/IMserver.php')
    # print(len(server.keys()))
    if len(server.keys()) == 1:
        server['user1'] = 'set'
        server['turn'] = '1'
        server['message'] = ''
        my_id = 1
    elif len(server.keys()) == 4:
        server['user2'] = 'set'
        my_id = 2
    else:
        print('Server is full. Try again later')
        sys.exit()

    my_turn = bool(my_id)

    loading = ""
    while len(server.keys()) == 4:
        print(f'Searching for second client {loading}', end='\r')
        if loading.count(".") <= 10:
            loading += "."
            time.sleep(1)
        else:
            print('timeout. Closing connection to server')
            server.clear()
            sys.exit()

    print(f'connected. Welcome to the Messaging System for Healthcare Professionals. You are user {my_id}\n')
    print('-------------------------------------------------------\n')
    received_message = ''
    server['conn'] = 'started'
    while server['conn'].decode().strip() != 'end':
        if str(my_id) in server['turn'].decode():
            myMessage = input("\nEnter a message to send to the other user: ")
            if myMessage == '\n' or myMessage == '':
                print(f'{colors.WARNING}Error. No message to send...{colors.ENDC}')
            elif len(server.keys()) == 2 or len(server.keys()) == 1:
                end_connection()
            else:
                server['message'] = myMessage.encode('UTF-8')
                if my_id == 1:
                    server['turn'] = '2'.encode('UTF-8')
                else:
                    server['turn'] = '1'.encode('UTF-8')
                print(f'{colors.BOLD}message sent{colors.ENDC}\n')
                time.sleep(0.1)
        else:
            print(f"{colors.UNDERLINE}Other user is typing...{colors.ENDC}", end='\r')
            time.sleep(1)
            if server['message'].decode() != '\n' and server['conn'].decode().strip() == 'started':
                print(f"{colors.BLUE}You have received a message.\n" +
                      f"{colors.CYAN}{server['message'].decode().strip()}{colors.ENDC}")
                server['message'] = ''

    end_connection()
except KeyboardInterrupt:
    end_connection()
