import random
import datetime
from socket import *

SERVER_NAME = "localhost"
SERVER_PORT = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

i = 1
while i < 11:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)

    start = datetime.datetime.now()
    message = str(i) + " " + start.strftime("%H:%M:%S %f")

    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        i += 1
        continue
    clientSocket.sendto(message.encode(), (SERVER_NAME, SERVER_PORT))
    i += 1
clientSocket.close()