from PyQt5.QtCore import QObject, pyqtSignal
from client import Client
import json


class ClientRepository(QObject):
    clients_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.clients = []
        self.load_clients()

    def load_clients(self):
        try:
            with open('client.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                print("Loaded data from client.json:", data)  # Debug statement
                self.clients = [Client.from_dict(item) for item in data]
                print("Clients loaded successfully:", self.clients)  # Debug statement
        except FileNotFoundError:
            print("client.json not found. Starting with an empty list.")  # Debug statement
            self.clients = []
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)  # Debug statement
            self.clients = []

        self.clients_updated.emit(self.clients)

    def save_clients(self):
        with open('client.json', 'w', encoding='utf-8') as file:
            data = [client.to_dict() for client in self.clients]
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_client(self, client):
        self.clients.append(client)
        self.save_clients()
        self.clients_updated.emit(self.clients)

    def get_clients(self):
        return self.clients