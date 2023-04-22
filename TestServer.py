from socket import *

#  Citation for the section before "try":
#  Date: 3/15/2023
#  Adapted from:
#  Kurose and Ross, Computer Networking: A Top-Down Approach, 8th Edition, Pearson

serverPort = 8889
serverUser = ''
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is online')

try:
    while True:
        connectionSocket, addr = serverSocket.accept()
        clientUser = connectionSocket.recv(4096).decode()
        # Using 4096 as size assuming messages will fit within that window.
        if clientUser == "/q":
            print("The client closed their connection prior to entering their name.")
            exit()
            connectionSocket.close()
            serverSocket.close()
        print(f"You are connected to {clientUser}")         # Message appears when client connects and provides a name
        serverUser = input("Please enter your name: ")      # No prompt for name until client connects
        if serverUser == "/q":                              # Server can quit prior to providing a name
            print(f"You have closed the server.")
            exit()
            connectionSocket.close()
            serverSocket.close()
        connectionSocket.send(serverUser.encode())

        while True:
            messageOut = input(f"To {clientUser}: ")        # Clarifies client name during messaging
            connectionSocket.send(messageOut.encode())
            if messageOut == "/q":                          # Server can quit at any time during conversation
                print(f"You have closed the server.")
                exit()
                connectionSocket.close()
                serverSocket.close()
            data = connectionSocket.recv(4096).decode()
            if data == "/q":
                print(f"{clientUser} has closed their connection.")
                exit()
                connectionSocket.close()
                serverSocket.close()
            print(f"From {clientUser}: {data}")             # Clarifies client name during messaging
except WindowsError:
    # Error provided when the client closes their connection prompts a windows error sometimes. This handles the exception
    print("It is likely the client closed their connection.")
    exit()
    serverSocket.close()

serverSocket.close()
