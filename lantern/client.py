import socket
import threading
from prompt_toolkit import print_formatted_text, PromptSession

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP = '127.0.0.1'
PORT = 8080
client.connect((IP, PORT))
print("Connected to server at " + IP + ":" + str(PORT))

session = PromptSession()
active = True

def message_handler():
    global active
    while active:
        message=client.recv(1024).decode('utf-8')
        if message == "__EXIT__":
            print("\nServer has exited the chat. Press Enter to exit.")
            active = False
            break
        else:       
            print_formatted_text(f"Server> {message}")

threading.Thread(target=message_handler, daemon=True).start()
while True:
    if not active:
        break
    send = session.prompt("Chat> ")
    if send.startswith("/"):
        if send == '/exit':
            client.send("__EXIT__".encode('utf-8'))
            print("Exiting chat.")
            active = False
            break
        elif send == '/help':
            print_formatted_text("Available commands:\n  /exit - Exit chat\n  /help - Show help")
            continue
    else:
        client.send(send.encode('utf-8'))

try:
    client.shutdown(socket.SHUT_RDWR)
except:
    pass
client.close()

