import customtkinter
import threading
from client import Client
from datetime import datetime

customtkinter.set_appearance_mode('Dark')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #welcome message
        welcomeMessage = 'Welcome to my communicator. Available commands: !nick <new nick>'

        # variable
        self.server_connected = False
        self.nick = 'Guest'
        self.DISCONNECT = 'Im leaving now by bye'
        self.client 

        # configure window
        self.geometry('600x400')
        self.title('Michaś komunikator')

        #bind items
        self.bind("<Return>", self.EnterAction)

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #create users frame
        self.userFrame = customtkinter.CTkFrame(self, width=150)
        self.userFrame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(5, 5), pady=(5, 5))
        self.userFrame.grid_rowconfigure(4, weight=1)

        #create messages frame
        self.textArea = customtkinter.CTkTextbox(self, width=400, height=500, state=customtkinter.DISABLED)
        self.textArea.grid(row=0, column=1, rowspan=3, columnspan=3, sticky="nsew", padx=(5, 5), pady=(5, 5))
        self.textArea.grid_rowconfigure(4, weight=1)

        #create widgets
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Message")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.sendButton = customtkinter.CTkButton(master=self, text='Send', fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.sendAction)
        self.sendButton.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.connectbutton = customtkinter.CTkButton(self, text='Connect', fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.connectToAServer)
        self.connectbutton.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.receive_thread = threading.Thread(target=self.get_data)
        self.receive_thread.start()

    def sendAction(self):
        try:
            value = self.entry.get()
            self.client.send(str(value))
            self.addMessage(value, 'message')
            self.entry.delete(0, 'end')
        except Exception as e:
            self.addMessage(f'Error: {e}', 'error')
    
    def EnterAction(self, event):
        self.sendAction()

    def connectToAServer(self):
        if(self.server_connected == False):
            try:
                self.client = Client()
                self.addMessage(f'Connection to server has been established', 'error')
                self.connectbutton.configure(text="Disconnect")
                self.server_connected = True
            except Exception as e:
                self.addMessage(f'{e}', 'error')
        else:
            try:
                self.client.client.close()
                self.addMessage(f'Connection to server has been ended', 'error')
                self.connectbutton.configure(text="Connect")
                self.server_connected = False
            except Exception as e:
                self.addMessage(f'{e}', 'error')
            
    
    def addMessage(self, message, type):
        self.now = datetime.now()
        self.date = self.now.strftime("%d.%m.%Y %H:%M:%S")
        self.textArea.configure(state=customtkinter.NORMAL)
        if(type == 'message'):
            self.textArea.insert(customtkinter.END, f'{self.date} {self.nick} - {message}' +'\n')
            if(message[0:5] == '!nick'):
                self.nick = message[6:]
                self.textArea.insert(customtkinter.END, '\033[1m' +f' Nick has been changed to: {self.nick}' +'\033[0m'  +'\n')
        elif(type == 'error'):
            self.textArea.insert(customtkinter.END, f'{self.date} {self.nick} - {message}' +'\n')
        else:
            print('yoyo')
        self.textArea.configure(state=customtkinter.DISABLED)

    def get_data(self):
        while self.server_connected:
            try:
                message = self.client.client.recv(1024).decode(self.FORMAT)
                if (message == self.DISCONNECT):
                    self.client.client.close()
                else:
                    self.addMessage(message, 'message')
            except:
                continue

if __name__ == "__main__":
    app = App()
    app.mainloop()