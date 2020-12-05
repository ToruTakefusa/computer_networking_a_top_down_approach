from socket import *
import datetime

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))
count = 1
serverSocket.settimeout(3)

while True:
    try:
        message, address = serverSocket.recvfrom(1024)
        client_count = int(message.split()[0])
        if count != client_count:
            print("packet lost\r\n")
            count = client_count + 1
        else:
            count += 1
    except timeout:
        print("The client is dead")
        serverSocket.close()
        exit(0)
