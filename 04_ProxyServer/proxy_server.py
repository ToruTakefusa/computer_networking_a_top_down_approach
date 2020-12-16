import socket
import sys
# import ssl

if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\nserver_ip: It is the IP Address Of Proxy Server')
    sys.exit(2)

SERVER_PORT = int(sys.argv[1])
SIZE = 4096
PORT_HTTPS = 443

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind(('', SERVER_PORT))
tcpSerSock.listen(1)

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(SIZE).decode()
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = False
    filetouse = "/" + filename
    print(filetouse)

    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = True

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send("ContentType:text/html\r\n".encode())
        for output in outputdata:
            tcpCliSock.send(output)
        f.close()
        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if not fileExist:
            # Create a socket on the proxyserver
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)

        try:
            # Connect to the socket to port 80
            # context = ssl.create_default_context()
            # wrapSocket = context.wrap_socket(c, server_hostname=hostn)
            # wrapSocket.connect((hostn, PORT_HTTPS))
            c.connect((hostn, 80))
            request = "GET "+"http://" + filename + " HTTP/1.0\r\nUser-Agent: Mozila/5.0\r\n\r\n"
            c.send(request.encode())
            content = c.recv(SIZE)

            # Create a new file in the cache for the requested file.
            # Also send the response in the buffer to client socket and the corresponding file in the cache
            tmpFile = open("./" + filename, "wb")
            tmpFile.write(content)
            tcpCliSock.send(content)
            tmpFile.close()
        except Exception as e:
            trace = sys.exc_info()[2]
            print("Exception happend!")
            print(e.with_traceback(trace))
            print("Illegal request")
    else:
        # HTTP response message for file not found
        tcpCliSock.send("HTTP/1.1 404 Not Found".encode())
        # Close the client and the server sockets
        tcpCliSock.close()
        # wrapSocket.close()
        c.close()
