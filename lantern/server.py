import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP = '127.0.0.1'
PORT = 8080
server.bind((IP, PORT))
print("Server started on " + IP + ":" + str(PORT))

server.listen(1)    #For P2P connections, can change it to () for Chat Room
clients = []

def send_message(user, message):
    pass

def client_handler(client):
    while True:
        username = client.recv(1024).decode('utf-8')

while True:
    client, address = server.accept()
    print(address[0] + " connected.")
    clients.append(client)
    threading.Thread(target=client_handler, args=(client,)).start()