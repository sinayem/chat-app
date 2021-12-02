import socket
import threading


HOST = '127.0.0.1'
PORT = 1234

LISTENER_LIMIT = 5

active_clients = []

def listen_for_message(client,username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message !='' :
            final_message = username + "~" + message
            send_message_to_all(final_message)
            
        else:
            print(f"The message from client {username} is empty")
            break

def send_message_to_single_client(client,message):
    client.sendall(message.encode())



def send_message_to_all(message):
    for user in active_clients:
        send_message_to_single_client(user[1],message)

def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username !='' :
            active_clients.append((username,client))
            prompt_message = "Server ~"+f"{username} added to the chat."
            send_message_to_all(prompt_message)
            break
        else:
            print("client username is empty")

    threading.Thread(target=listen_for_message,args=(client,username,)).start()


def main():
    #creating the socket class object
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((HOST,PORT))
        print("Server is running")
    except:
        print(f"unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:
        client,address = server.accept()
        print(f"successfully connected to client {address[0]}{address[1]}")

        threading.Thread(target=client_handler,args=(client,)).start()

if __name__ == '__main__':
    main()