from client_repository import ClientRepository
from client_view import ClientTableView, ClientFormDialog, EditClientDialog, AllClientDetailsDialog
from PyQt5.QtWidgets import QMessageBox
from client import Client

class ClientController:
    def __init__(self):
        self.repository = ClientRepository()
        self.view = ClientTableView(self)

        self.repository.clients_updated.connect(self.view.update_table)

        self.view.update_table(self.repository.get_clients())

    def show_add_client_dialog(self):
        dialog = ClientFormDialog()
        if dialog.exec_():
            client_data = dialog.get_client_data()
            if self.validate_client_data(client_data):
                client = Client(**client_data)
                if not self.repository.is_phone_unique(client.Phone):
                    QMessageBox.warning(self.view, 'Номер телефона уже существует', 'Номер должен быть уникальным')
                else:
                    self.repository.add_client(client)

    def show_edit_client_dialog(self, index):
        clients = self.repository.get_clients()
        if 0 <= index < len(clients):
            client = clients[index]
            dialog = EditClientDialog(client)
            if dialog.exec_():
                updated_client_data = dialog.get_client_data()
                if self.validate_client_data(updated_client_data):
                    updated_client = Client(**updated_client_data)
                    if updated_client.Phone != client.Phone and not self.repository.is_phone_unique(updated_client.Phone):
                        QMessageBox.warning(self.view, 'Номер телефона уже существует', 'Номер должен быть уникальным')
                    else:
                        self.repository.update_client(index, updated_client)

    def delete_client(self, index):
        if 0 <= index < len(self.repository.get_clients()):
            self.repository.delete_client(index)
        else:
            QMessageBox.warning(self.view, 'Клиент не выбран', 'Выберите клиента для удаления')

    def sort_clients(self, field):
        self.repository.sort_by_field(field)

    def show_all_client_details(self):
        clients = self.repository.get_clients()
        dialog = AllClientDetailsDialog(clients, self)
        dialog.exec_()

    def validate_client_data(self, client_data):
        if not all(client_data.values()):
            QMessageBox.warning(self.view, 'Ошибка', 'Все поля должны быть заполнены')
            return False
        return True

    def run(self):
        self.view.show()