import socket
import sys
import os
import ssl


def get_response(sock, host, filename):
    sock.connect((host, 80))
    socket_file = sock.makefile("wrb", 0)
    request = "GET " + "http://" + filename + " HTTP/1.0\r\nUser-Agent: Mozila/5.0\r\n\r\n"
    socket_file.write(request.encode())
    socket_file.flush()
    response = socket_file.read()
    if not response:
        raise ValueError("Cannot receive response.")
    return response


def read_from_cache(file_to_use):
    with open(file_to_use, "r") as f:
        return f.readlines()


def send_cache(socket, file_to_use):
    # ProxyServer finds a cache hit and generates a response message
    socket.send("HTTP/1.1 200 OK\r\n".encode())
    socket.send("ContentType:text/html\r\n".encode())
    output_data = read_from_cache(file_to_use)
    for output in output_data:
        socket.send(output.encode())
    print('Read from cache')


if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\nserver_ip: It is the IP Address Of Proxy Server')
    sys.exit(2)

SERVER_PORT = int(sys.argv[1])
SIZE = 4096
PORT_HTTPS = 443

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
tcpSerSock.bind(('', SERVER_PORT))
tcpSerSock.listen(1)

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(SIZE).decode()
    print(message)
    if message == "" or ('.com' not in message):
        continue

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = False
    file_to_use = ("/" + filename)[1:]
    print(file_to_use)

    try:
        # Check whether the file exist in the cache
        if os.path.isfile(file_to_use):
            try:
                send_cache(tcpCliSock, file_to_use)
            finally:
                tcpCliSock.close()
        else:
            # Create a socket on the proxy server
            host_name = filename.replace("www.", "", 1)
            print(host_name)

            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Create a new file in the cache for the requested file.
                tmpFile = open("./" + filename, "wb")
                content = get_response(c, host_name, filename)
                tmpFile.write(content)
                tcpCliSock.send(content)
            except Exception as e:
                trace = sys.exc_info()[2]
                print(e.with_traceback(trace))
            finally:
                tmpFile.close()
                c.close()
                tcpCliSock.close()
    except IOError:
        # HTTP response message for file not found
        print("IOError")
        tcpCliSock.send("HTTP/1.1 404 Not Found".encode())
        # Close the client and the server sockets
        tcpCliSock.close()
