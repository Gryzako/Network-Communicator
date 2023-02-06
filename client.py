import socket
from tkinter import *

class Client():

    def __init__(self):
        PORT = 5050
        self.FORMAT = 'utf-8'
        SERVER = ''
        ADDR = (SERVER, PORT)
        self.messages_from_client = []
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def send(self, msg):
            message = msg.encode(self.FORMAT)
            self.client.send(message)
        

            

