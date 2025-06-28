import socket
import threading
from prompt_toolkit import PromptSession, print_formatted_text
from lantern.mdns import update_status


active = True

def receiver():
    global active
    session = PromptSession()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    IP = '0.0.0.0'
    PORT = 8090
    print("\nServer.py Test\n")
    server.bind((IP, PORT))
    print("Server started on " + IP + ":" + str(PORT))
    server.listen(1)

    client, address = server.accept()
    print(address[0] + " connected.")
    update_status("Busy")

    def message_handler():
        global active
        while active:
            message=client.recv(1024).decode('utf-8')
            if message == "__EXIT__":
                print("\nClient has exited the chat. Press Enter to exit.")
                update_status("Active")
                active = False
                break
            else:
                print_formatted_text(f"Client> {message}")

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
                print("Unknown command. Type /help for available commands.")
                continue
        else:
            client.send(send.encode('utf-8'))

    try:
        client.shutdown(socket.SHUT_RDWR)
        server.shutdown(socket.SHUT_RDWR)
    except:
        pass
    server.close()
    client.close()