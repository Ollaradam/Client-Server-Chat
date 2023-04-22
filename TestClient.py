from socket import *

#  Citation for the section before "try":
#  Date: 3/15/2023
#  Adapted from:
#  Kurose and Ross, Computer Networking: A Top-Down Approach, 8th Edition, Pearson

serverName = 'localhost'
serverPort = 8889
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientUser = input("Please enter your name: ")
if clientUser == "/q":                                      # Client can close their connection prior to giving a name
    print(f"You have exited the chat.")
    clientSocket.send(clientUser.encode())
    exit()
    clientSocket.close()

try:
    while True:
        clientSocket.send(clientUser.encode())
        serverUser = clientSocket.recv(4096).decode()
        # Using 4096 as size assuming messages will fit within that window.
        if serverUser:
            print(f"You are connected to {serverUser}")
            while True:
                data = clientSocket.recv(4096).decode()
                if data == "/q":
                    print(f"{serverUser} has closed their connection.")
                    exit()
                    clientSocket.close()
                print(f"From {serverUser}: {data}")         # Clarifies server user name during messaging
                messageOut = input(f"To {serverUser}: ")    # Clarifies server user name during messaging
                if messageOut == "/q":                      # Client can close connection any time
                    print(f"You have exited the chat.")
                    clientSocket.send(messageOut.encode())
                    exit()
                    clientSocket.close()
                clientSocket.send(messageOut.encode())
except WindowsError:
    # Error provided when the server closes their connection prompts a windows error sometimes. This handles the exception
    print("It is likely the server has been closed.")

clientSocket.close()
