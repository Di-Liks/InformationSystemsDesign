from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QDialog, QFormLayout, QLineEdit, QLabel, QMessageBox, QHBoxLayout
)
from client import Client

class ClientTableView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Лист клиентов')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Last Name', 'Phone'])

        self.add_button = QPushButton('Добавить клиента', self)
        self.add_button.clicked.connect(self.controller.show_add_client_dialog)

        self.view_details_button = QPushButton('Посмотреть всю информацию', self)
        self.view_details_button.clicked.connect(self.show_all_client_details)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.view_details_button)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_table(self, clients):
        self.table.setRowCount(len(clients))
        for i, client in enumerate(clients):
            self.table.setItem(i, 0, QTableWidgetItem(client.LastName))
            self.table.setItem(i, 1, QTableWidgetItem(client.Phone))

    def show_all_client_details(self):
        clients = self.controller.repository.get_clients()
        dialog = AllClientDetailsDialog(clients)
        dialog.exec_()

class AllClientDetailsDialog(QDialog):
    def __init__(self, clients, parent=None):
        super().__init__(parent)
        self.clients = clients
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Полная информация')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Last Name', 'First Name', 'Middle Name', 'Address', 'Phone'])

        self.update_table(self.clients)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def update_table(self, clients):
        self.table.setRowCount(len(clients))
        for i, client in enumerate(clients):
            self.table.setItem(i, 0, QTableWidgetItem(client.LastName))
            self.table.setItem(i, 1, QTableWidgetItem(client.FirstName))
            self.table.setItem(i, 2, QTableWidgetItem(client.MiddleName))
            self.table.setItem(i, 3, QTableWidgetItem(client.Address))
            self.table.setItem(i, 4, QTableWidgetItem(client.Phone))

class ClientDetailsDialog(QDialog):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client = client
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Client Details')
        self.layout = QFormLayout(self)

        self.last_name_label = QLabel(self.client.LastName, self)
        self.first_name_label = QLabel(self.client.FirstName, self)
        self.middle_name_label = QLabel(self.client.MiddleName, self)
        self.address_label = QLabel(self.client.Address, self)
        self.phone_label = QLabel(self.client.Phone, self)

        self.layout.addRow('Last Name:', self.last_name_label)
        self.layout.addRow('First Name:', self.first_name_label)
        self.layout.addRow('Middle Name:', self.middle_name_label)
        self.layout.addRow('Address:', self.address_label)
        self.layout.addRow('Phone:', self.phone_label)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

class ClientFormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Client Form')
        self.layout = QFormLayout(self)

        self.last_name = QLineEdit(self)
        self.first_name = QLineEdit(self)
        self.middle_name = QLineEdit(self)
        self.address = QLineEdit(self)
        self.phone = QLineEdit(self)

        self.layout.addRow('Last Name', self.last_name)
        self.layout.addRow('First Name', self.first_name)
        self.layout.addRow('Middle Name', self.middle_name)
        self.layout.addRow('Address', self.address)
        self.layout.addRow('Phone', self.phone)

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

    def get_client(self):
        return Client(
            LastName=self.last_name.text(),
            FirstName=self.first_name.text(),
            MiddleName=self.middle_name.text(),
            Address=self.address.text(),
            Phone=self.phone.text()
        )