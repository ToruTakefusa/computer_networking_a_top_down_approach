from socket import *
from datetime import datetime

serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

i = 1
minimum = 100
maximum = 0
sum = 0
succceed = 0

while i < 11:
    try:
        start = datetime.now()
        message = "Ping " + str(i) + " " + start.strftime("%H:%M:%S %f")
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())

        end = datetime.now()
        diff = (end - start).total_seconds()
        minimum = min(minimum, diff)
        maximum = max(maximum, diff)
        sum += diff
        succceed += 1
        print(diff)
    except timeout:
        print("Request timed out")
    finally:
        i = i + 1
print("min: " + str(minimum))
print("max " + str(maximum))
average = sum / succceed
print("average: " + str(average))
loss = (10 - succceed) / 10 * 100
print("packet loss rate: " + str(loss) + "%")
clientSocket.close()
