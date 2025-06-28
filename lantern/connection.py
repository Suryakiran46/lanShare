import socket
from lantern.server import receiver
from lantern.client import sender

def close_connection():
    pass

def request(ip, name, status):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080
    client.connect((ip, port))
    client.send(f"Connection request from {name} (Y/n): ".encode('utf-8'))
    reply = client.recv(1024).decode('utf-8')
    print("\nRequest Test\n")
    if reply.lower() == "y":
        print(f"Chat session started with {name} at {ip}.")
        sender(ip)
    else:
        print(f"Chat session declined by {name} at {ip}.")
        

def request_handler():
    ip = '0.0.0.0'
    port = 8080
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((ip, port))
    listener.listen()
    while True:
        client, address = listener.accept()
        client_ip = address[0]
        message = client.recv(1024).decode('utf-8')
        reply = input(message)
        print("\n",reply," : Reply Test\n")
        client.send(reply.encode('utf-8'))

        if reply.lower() == 'y':
            client.close()
            listener.close()
            receiver()

    
