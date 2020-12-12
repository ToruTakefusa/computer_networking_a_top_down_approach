import socket
import sys

SERVER_NAME = sys.argv[1]
SERVER_PORT = sys.argv[2]
YOUR_ADDRESS = sys.argv[3]
TO_ADDRESS = sys.argv[4]
MESSAGE = "\r\n I love computer networks!"
END_MESSAGE = "\r\n.\r\n"
SIZE = 1024


def send(client_socket, message):
    client_socket.send(message.encode())


def receive(client_socket, status_code):
    recv = client_socket.recv(SIZE).decode()
    if recv[:3] != str(status_code):
        print(str(status_code) + ' reply not received from server.')
        print(recv)

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = (SERVER_NAME, int(SERVER_PORT))
# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(mailserver)
receive(clientSocket, 220)

# Send HELO command and print server response.
send(clientSocket, 'HELO Alice\r\n')
receive(clientSocket, 250)

# Send MAIL FROM command and print server response.
fromCommand = 'MAIL FROM: <' + YOUR_ADDRESS + '>\r\n'
send(clientSocket, fromCommand)
receive(clientSocket, 250)

# Send RCPT TO command and print server response.
rcptCommand = 'RCPT TO: <' + TO_ADDRESS + '>\r\n'
send(clientSocket, rcptCommand)
receive(clientSocket, 250)

# Send DATA command and print server response.
send(clientSocket, 'DATA\r\n')
receive(clientSocket, 354)

# Send message data.
send(clientSocket, MESSAGE)
# Message ends with a single period.
send(clientSocket, END_MESSAGE)
receive(clientSocket, 250)

# Send QUIT command and get server response.
send(clientSocket, 'QUIT\r\n')
receive(clientSocket, 221)