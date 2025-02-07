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
                self.clients = [Client.from_dict(item) for item in data]
        except FileNotFoundError:
            print("client.json not found. Starting with an empty list.")
            self.clients = []
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            self.clients = []

        self.clients_updated.emit(self.clients)

    def save_clients(self):
        with open('client.json', 'w', encoding='utf-8') as file:
            data = [client.to_dict() for client in self.clients]
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_client(self, client):
        if not self.is_phone_unique(client.Phone):
            return False
        self.clients.append(client)
        self.save_clients()
        self.clients_updated.emit(self.clients)
        return True

    def update_client(self, index, client):
        if index < 0 or index >= len(self.clients):
            return False
        self.clients[index] = client
        self.save_clients()
        self.clients_updated.emit(self.clients)
        return True

    def delete_client(self, index):
        if index < 0 or index >= len(self.clients):
            return False
        self.clients.pop(index)
        self.save_clients()
        self.clients_updated.emit(self.clients)
        return True

    def is_phone_unique(self, phone):
        return all(client.Phone != phone for client in self.clients)

    def get_clients(self):
        return self.clients