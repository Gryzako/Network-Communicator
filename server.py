from concurrent.futures import thread
import socket
import threading

PORT = 5050
SERVER = '192.168.0.66'
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnected!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = []

def broadcast(message):
    for client in clients:
        client.send(message)    
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            break
        
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        clients.append(client)
        client.send('Connected to the server!'.encode(FORMAT))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
        print(f"[Active Connections] {threading.activeCount() -1}")
        
receive()       
