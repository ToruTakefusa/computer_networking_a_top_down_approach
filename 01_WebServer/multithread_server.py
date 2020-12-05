from socket import *
import threading
import traceback
import os


def handle_request(connection_socket):
    try:
        message = connection_socket.recv(1024).decode()
        filename = "/" + os.getcwd() + message.split()[1]
        f = open(filename[1:], "r")
        output = f.read()
        connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
        connection_socket.send("Server: Python\r\n".encode())
        connection_socket.send("Content-Type: text/html\r\n".encode())
        connection_socket.send("\r\n".encode())

        for i in range(0, len(output)):
            connection_socket.send(output[i].encode())

        connection_socket.send("\r\n".encode())
        connection_socket.close()
    except IOError:
        print(traceback.format_exc())
        connection_socket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connection_socket.send("Server: Python\r\n".encode())
        connection_socket.send("Content-Type: text/html\r\n".encode())
        connection_socket.send("\r\n".encode())
        # show message
        connection_socket.send("<html>\r\n".encode())
        connection_socket.send("<head></head>\r\n".encode())
        connection_socket.send("<body>404 Not Found</body>\r\n".encode())
        connection_socket.send("</html>".encode())
        connection_socket.close()


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print('Ready to serve...')
    connection_socket, addr = serverSocket.accept()
    t = threading.Thread(target=handle_request, args=(connection_socket, )).start()
