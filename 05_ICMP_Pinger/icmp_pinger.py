from socket import *
import os
import sys
import struct
import time
import select
import binascii
ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        this_val = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + this_val
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, id, timeout, dest_addr):
    time_left = timeout

    while True:
        started_select = time.time()
        what_ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = (time.time() - started_select)
        if not what_ready[0]:  # Timeout
            return "Request timed out."
        else:
            break

    time_received = time.time()
    rec_packet, addr = my_socket.recvfrom(1024)

    # Fill in start
    print("receive_one_ping")
    # Fetch the ICMP header from the IP packet
    # rec_packet contains IP packet
    reply = rec_packet[20:]
    reply_header = reply[0:8]
    # The type value is wrong. Maybe, it's not type value.
    (icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence) = struct.unpack("bbHHh", reply_header)
    print(icmp_type)
    print(icmp_code)
    print(icmp_checksum)
    print(icmp_id)
    print(icmp_sequence)
    # Fill in end

    time_left = time_left - how_long_in_select

    if time_left <= 0:
        return "Request timed out."


def send_one_ping(my_socket, dest_addr, id):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy header with a 0 checksum
    # struct interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, id, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(str(header + data))

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16bit integers from host to network byte order
        my_checksum = htons(my_checksum) & 0xffff
    else:
        my_checksum = htons(my_checksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, id, 1)
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1))  # AF_INET address must be tuple, not str

    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def do_one_ping(dest_addr, timeout):
    icmp = getprotobyname("icmp")

    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    my_socket = socket(AF_INET, SOCK_RAW, icmp)
    my_id = os.getpid() & 0xFFFF  # Return the current process id
    send_one_ping(my_socket, dest_addr, my_id)
    delay = receive_one_ping(my_socket, my_id, timeout, dest_addr)
    my_socket.close()

    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost

    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

    # Send ping requests to a server separated by approximately one second
    while 1:
        delay = do_one_ping(dest, timeout)
        print(delay)
        time.sleep(1)  # one second

    return delay


# ping("google.com")
ping("127.0.0.1")
