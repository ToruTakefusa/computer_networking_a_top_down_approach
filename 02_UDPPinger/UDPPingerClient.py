from socket import *
from datetime import datetime

serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

i = 1
while i < 11:
    try:
        start = datetime.now()
        message = "Ping " + str(i) + " " + start.strftime("%H:%M:%S %f")
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())

        end = datetime.now()
        diff = (end - start).total_seconds()
        diff.set_printptions(suppress = True)
        print(diff)
    except timeout:
        print("Request timed out")
    finally:
        i = i + 1
clientSocket.close()