import socket
import threading
from time import sleep
from prompt_toolkit import print_formatted_text, PromptSession
from lantern.mdns import update_status

active = True

def sender(IP): 
    global active
    session = PromptSession()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
   #Receivers IP
    PORT = 8090
    print("\nClient.py Test\n")
    sleep(10)
    client.connect((IP, PORT))
    print("Connected to server at " + IP + ":" + str(PORT))
    
    update_status("Busy")

    def message_handler():
        global active
        while active:
            message=client.recv(1024).decode('utf-8')
            if message == "__EXIT__":
                print("\nServer has exited the chat. Press Enter to exit.")
                update_status("Active")
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
                update_status("Active")
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
    

