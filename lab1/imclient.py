import sys

import im
import time

server = im.IMServerProxy('https://web.cs.manchester.ac.uk/t11915jr/COMP28112/lab1/IMserver.php')
# print(len(server.keys()))
if len(server.keys()) == 1:
    server['user1'] = 'set'
    my_id = 1
elif len(server.keys()) == 2:
    server['user2'] = 'set'
    my_id = 2
else:
    print('Server is full. Try again later')
    sys.exit()

my_turn = bool(my_id)

loading = ""
while len(server.keys()) == 2:
    print(f'Searching for second client {loading}', end='\r')
    if loading.count(".") <= 6:
        loading += "."
        time.sleep(1)
    else:
        print('timeout. Closing connection to server')
        server.clear()
        sys.exit()

print('connected')
while server['user1'] == server['user2']:
    time.sleep(5)

print("connection to server ended.")
server.clear()
