import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f'Server listening on {HOST}:{PORT}')

clients = []
aliases = []

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            broadcast(message, client_socket)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat.'.encode('utf-8'), client_socket)
            aliases.remove(alias)
            break

def receive_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address}')

        client_socket.send('NICKNAME'.encode('utf-8'))
        alias = client_socket.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client_socket)

        print(f'Nickname of the client is {alias}')
        broadcast(f'{alias} has joined the chat.'.encode('utf-8'), client_socket)
        client_socket.send('You are now connected!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

receive_connections()
