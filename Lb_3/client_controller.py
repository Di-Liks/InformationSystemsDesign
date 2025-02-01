from client_repository import ClientRepository
from client_view import ClientTableView, ClientFormDialog

class ClientController:
    def __init__(self):
        self.repository = ClientRepository()
        self.view = ClientTableView(self)
        self.repository.clients_updated.connect(self.view.update_table)

    def show_add_client_dialog(self):
        dialog = ClientFormDialog()
        if dialog.exec_():
            client = dialog.get_client()
            self.repository.add_client(client)

    def run(self):
        self.view.show()