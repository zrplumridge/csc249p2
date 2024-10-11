#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)

def parse_message(message):
    #print("Message to be parsed")
    message = message.decode("utf-8")
    #print("Message decoded: " + message)
    message = message.split(" ", 2)
    SERVER_IP, SERVER_PORT, *message = message
    message = str(message)
    #print("Server IP: " + SERVER_IP)
    #print("Server port: " + SERVER_PORT)
    #print(message)
    #print("Message: " + message)
    #SERVER_IP = float.from_bytes(SERVER_IP)
    SERVER_PORT = int(SERVER_PORT)
    # Parse the application-layer header into the destination SERVER_IP, destination SERVER_PORT,
    # and message to forward to that destination
    return SERVER_IP, SERVER_PORT, message

### INSTRUCTIONS ###
# The VPN, like the server, must listen for connections from the client on IP address
# VPN_IP and port VPN_port. Then, once a connection is established and a message recieved,
# the VPN must parse the message to obtain the server IP address and port, and, without
# disconnecting from the client, establish a connection with the server the same way the
# client does, send the message from the client to the server, and wait for a reply.
# Upon receiving a reply from the server, it must forward the reply along its connection
# to the client. Then the VPN is free to close both connections and exit.

# The VPN server must additionally print appropriate trace messages and send back to the
# client appropriate error messages.

print("server starting - listening for connections at IP", VPN_IP, "and port", VPN_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((VPN_IP, VPN_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data: #if no data present here / empty
                break
            #confirms receipt of message
            print(f"Received client message: '{data!r}' [{len(data)} bytes]")
            SERVER_IP, SERVER_PORT, message = parse_message(data)

            print("VPN connecting to server at IP", SERVER_IP, "and port", SERVER_PORT)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_IP, SERVER_PORT))
                MSG = message
                print(f"connection established, sending message '{MSG}'")
                s.sendall(bytes(MSG, 'utf-8'))
                print("message sent, waiting for reply")
                data = s.recv(1024)

            print("Received response from server. Returning to client.")

            conn.sendall(data)
            conn.close()


print("VPN is done!")
