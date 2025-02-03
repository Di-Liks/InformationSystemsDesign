from client_repository import ClientRepository
from client_view import ClientTableView, ClientFormDialog
from PyQt5.QtWidgets import QMessageBox

class ClientController:
    def __init__(self):
        self.repository = ClientRepository()
        self.view = ClientTableView(self)

        self.repository.clients_updated.connect(self.view.update_table)

        self.view.update_table(self.repository.get_clients())

    def show_add_client_dialog(self):
        dialog = ClientFormDialog()
        if dialog.exec_():
            client = dialog.get_client()
            if not self.repository.is_phone_unique(client.Phone):
                QMessageBox.warning(self.view, 'Номер телефона уже существует', 'Номер должен быть уникальным')
            else:
                self.repository.add_client(client)

    def run(self):
        self.view.show()