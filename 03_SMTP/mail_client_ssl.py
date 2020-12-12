import socket
import ssl
import sys
import base64
import time

SERVER_NAME = 'smtp.gmail.com'
SERVER_PORT = 465
USER = sys.argv[1]
PASSWORD = sys.argv[2]
FROM_ADDRESS = sys.argv[3]
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


# Create socket called clientSocket and establish a TCP connection with mail server
context = ssl.create_default_context()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bare_client:
    with context.wrap_socket(bare_client, server_hostname=SERVER_NAME) as client:
        client.connect((SERVER_NAME, SERVER_PORT))
        receive(client, 220)

        send(client, 'EHLO example.com\r\n')
        receive(client, 250)

        send(client, 'AUTH LOGIN\r\n')
        receive(client, 334)
        send(client, base64.b64encode(USER.encode()).decode() + '\r\n')
        receive(client, 334)

        send(client, base64.b64encode(PASSWORD.encode()).decode() + '\r\n')
        receive(client, 235)

        # Send MAIL FROM command and print server response.
        fromCommand = 'MAIL FROM: <' + FROM_ADDRESS + '>\r\n'
        send(client, fromCommand)
        receive(client, 250)

        # Send RCPT TO command and print server response.
        rcptCommand = 'RCPT TO: <' + TO_ADDRESS + '>\r\n'
        send(client, rcptCommand)
        receive(client, 250)

        # Send DATA command and print server response.
        send(client, 'DATA\r\n')
        receive(client, 354)

        # Send message data.
        send(client, 'From user1 <' + FROM_ADDRESS + '>\r\n')
        send(client, 'To: user2 <' + TO_ADDRESS + '>\r\n')
        send(client, 'Date: ' + time.asctime(time.localtime(time.time())) + '\r\n')
        send(client, 'Subject: Test\r\n')
        send(client, '\r\n')
        send(client, MESSAGE)

        # Message ends with a single period.
        send(client, END_MESSAGE)
        receive(client, 250)

        send(client, 'QUIT\r\n')
        receive(client, 221)