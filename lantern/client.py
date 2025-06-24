import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP = '127.0.0.1'
PORT = 8080
client.connect((IP, PORT))
print("Connected to server at " + IP + ":" + str(PORT))
