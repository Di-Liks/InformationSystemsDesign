from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QDialog, QFormLayout, QLineEdit
)
from client import Client  # Import the Client class

class ClientTableView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Client List')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Last Name', 'Phone'])

        self.add_button = QPushButton('Add Client', self)
        self.add_button.clicked.connect(self.controller.show_add_client_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_table(self, clients):
        self.table.setRowCount(len(clients))
        for i, client in enumerate(clients):
            self.table.setItem(i, 0, QTableWidgetItem(client.LastName))
            self.table.setItem(i, 1, QTableWidgetItem(client.Phone))

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