import socket
import sys

SERVER_NAME = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
FILE = sys.argv[3]

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((SERVER_NAME, SERVER_PORT))
clientSocket.send(("GET /" + FILE + " HTTP/1.1\r\n").encode())
clientSocket.send(("Host: " + SERVER_NAME + ": " + str(SERVER_PORT) + "\r\n").encode())
clientSocket.send("Accept: text/html\r\n".encode())
clientSocket.send("Accept-Language en\r\n".encode())
clientSocket.send("Content-Type: text/html".encode())
clientSocket.send("Connection: keep-alive".encode())

message = clientSocket.recv(1024)
print(message)
clientSocket.close()