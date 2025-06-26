import socket


def close_connection():
    pass

def request(ip, name, status):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080
    client.connect((ip, port))
    client.send(f"Connection request from {name} (Y/n): ".encode('utf-8'))
    reply = client.recv(1024).decode('utf-8')
    if reply.lower() == "y":
        print(f"Chat session started wsith {name} at {ip}.")
    else:
        print(f"Chat session declined by {name} at {ip}.")
        

def request_handler():
    ip = '0.0.0.0'
    port = 8080
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((ip, port))
    listener.listen()
    client, address = listener.accept()
    message = client.recv(1024).decode('utf-8')
    reply = input(message)

    if reply.lower() == 'y':
        pass                    # Check if its bussy, if its busy, close the connection
                                # Otherwise, start the chat session

    client.send(reply.encode('utf-8'))
    client.close()
    listener.close()