#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 echo-server.py --help' to see what these lines do
parser = argparse.ArgumentParser('Starts a server that returns the data sent to it unmodified')
parser.add_argument('--server_IP', help='IP address at which to host the server', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which to host the server', **arguments.server_port_arg)
args = parser.parse_args()

SERVER_IP = args.server_IP  # Address to listen on
SERVER_PORT = args.server_port  # Port to listen on (non-privileged ports are > 1023)

print("server starting - listening for connections at IP", SERVER_IP, "and port", SERVER_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            #confirms receipt of message
            print(f"Received client message: '{data!r}' [{len(data)} bytes]")
            #calculates number of times to repeat output based on first character
            length = int.from_bytes(data[:1], byteorder="little") - 48
            #if first character is not a number, will default to 5 repeats
            if length > 20:
                length = 5
            print(f"Times to be repeated is '{length!r}'")

            #converts lowercase values to uppercase
            data = data[1:].upper() #+ bytes('', 'utf-8')

            #loops through to send output multiple times
            for x in range(length):
                print(f"echoing '{data!r}' back to client")
                conn.send(data)

            conn.close()

print("server is done!")
