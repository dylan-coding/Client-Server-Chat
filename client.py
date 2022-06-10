# Author: Dylan Smith
# Last Modified: 3/12/2022
# Description: Acts as a client interface for a chat program, allowing the
# user to connect to a server and chat with the user at the server.

# Sources Cited: The following commented sections cite the source of verbatim
#               code or inspiration for modified code.
# Title: Socket Programming HOWTO
# Author: Gordon McMillan
# Date: Mar 12, 2022
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


def make_connection():
    """
    Establishes a connection to the server specified at host:port.
    :return: client: Socket connection to server
    """
    # Create the socket and connect to the host at specified port
    client = socket(AF_INET, SOCK_STREAM)
    # Host and port information
    host = 'localhost'
    port = 2022
    # Attempt connection to server and print instructions to Client user
    client.connect((host, port))
    print("Connected to:", host, "on port:", port)
    print("Type /q to quit")
    print("Enter a message to send...")
    return client
        
    
def chat_loop(server):
    """
    Loops chat with server until either side terminates with '/q'.
    :param server: Socket connection to server
    :return: None
    """
    message = ''
    while message != '/q':
        # Loop until user types '/q' or the server closes the chat
        message = input('>')
        if message == '/q':
            # Client user has requested termination of chat
            print('Connection closed.')
            server.send(message.encode())
        else:
            # Send message to server
            server.send(message.encode())
            # Receive response and decode for console printing
            response = server.recv(1024).decode()
            if response != '/q':
                # Print response from server
                print(response)
            else:
                # Server has terminated the chat
                message = '/q'
                print("Session closed by server.")
    server.close()


if __name__ == '__main__':
    # Create server upon program start
    socket = make_connection()
    # Establish chat loop
    chat_loop(socket)
