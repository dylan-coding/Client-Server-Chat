# Author: Dylan Smith
# Last Modified: 3/12/2022
# Description: Acts as a server for a chat program, waiting for a client to
# connect and then allowing a two-way communication channel between the
# Client user and the Server user.

# Sources Cited: The following commented sections cite the source of verbatim
#               code or inspiration for modified code.
# Title: Socket Programming HOWTO
# Author: Gordon McMillan
# Date: Jan 20, 2022
# Code Version: Unknown
# Type: Source code
# Availability: https://docs.python.org/3/howto/sockets.html

# Title: Socket Programming in Python (Guide)
# Author: Nathan Jennings
# Date: Mar 12, 2022
# Code Version: Unknown
# Type: Guide
# Availability: https://realpython.com/python-sockets/

from socket import *  # For socket use


def make_server():
    """
    Creates a socket bound to localhost:2022 and listens for a connection
    :return: a socket connection to the client
    """
    server = socket(AF_INET, SOCK_STREAM)
    # Create server and establish listening socket
    server.bind(('localhost', 2022))
    server.listen(1)
    print("Server listening on: localhost on port: 2022")
    return server


def chat_loop(server):
    """
    Prints the message sent by the client and prompts for a reply, looping
    until the user responds with '/q'.
    :param server: The socket bound to localhost that a client has connected to
    :return: None
    """
    reply = ''
    # Accept connection
    (connection, address) = server.accept()
    print("Connected by", address)
    # Wait for first message from client
    print("Waiting for message...")
    message = connection.recv(1024).decode()
    if message != '/q':
        # Print message from Client and instructions to Server user
        print(message)
        print("Type /q to quit")
        print("Enter message to send...")
        while reply != '/q':
            # Loop until server or client user responds with '/q'
            reply = send_message(connection)
    else:
        # Client has terminated the chat
        print('Connection closed by client.')
    connection.close()
    

def send_message(connection):
    """
    Prompts user for a message to send to client, encodes, and sends.
    :param connection: Socket connection to client
    :return: reply: The user's response to the client
    """
    reply = input('>')
    # Send message to Client
    connection.send(reply.encode())
    if reply != '/q':
        # Wait for response from Client
        reply = receive_message(connection)
    else:
        # Server sent close message to Client
        print('Connection closed.')
    return reply


def receive_message(connection):
    """
    Receives message from client user and decodes it for printing
    :param connection: Socket connection to the client
    :return: reply: Server user's response to the client
    :return: message: Client user's termination request, supersedes reply
    """
    message = connection.recv(1024).decode()
    if message == '/q':
        # Client has terminated the chat
        print('Session closed by client.')
        return message  # Returns '/q' to terminated chat_loop
    print(message)
    # Get message to send back to Client user
    reply = send_message(connection)
    return reply


if __name__ == '__main__':
    # Create server upon program start
    skt = make_server()
    # Open chat loop with client
    chat_loop(skt)
