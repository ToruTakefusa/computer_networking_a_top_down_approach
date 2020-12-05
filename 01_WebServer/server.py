from socket import *
import sys
import traceback
import os

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = "/" + os.getcwd() + message.split()[1]
        f = open(filename[1:], "r")
        outputdata = f.read()
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Server: Python\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode())

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        print(traceback.format_exc())
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Server: Python\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode())
        # show message
        connectionSocket.send("<html>\r\n".encode())
        connectionSocket.send("<head></head>\r\n".encode())
        connectionSocket.send("<body>404 Not Found</body>\r\n".encode())
        connectionSocket.send("</html>".encode())
        connectionSocket.close()

        serverSocket.close()
        sys.exit()
