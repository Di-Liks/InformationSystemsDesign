from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QDialog, QFormLayout, QLineEdit, QLabel, QMessageBox, QHBoxLayout
)

class ClientTableView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Список клиентов')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Last Name', 'Phone'])

        self.add_button = QPushButton('Добавить клиента', self)
        self.add_button.clicked.connect(self.controller.show_add_client_dialog)

        self.view_details_button = QPushButton('Подробнее', self)
        self.view_details_button.clicked.connect(self.controller.show_all_client_details)

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

class AllClientDetailsDialog(QDialog):
    def __init__(self, clients, controller, parent=None):
        super().__init__(parent)
        self.clients = clients
        self.controller = controller
        self.initUI()

        self.controller.repository.clients_updated.connect(self.update_table)

    def initUI(self):
        self.setWindowTitle('Детальная информация')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Last Name', 'First Name', 'Middle Name', 'Address', 'Phone'])

        self.update_table(self.clients)

        self.edit_button = QPushButton('Изменить клиента', self)
        self.edit_button.clicked.connect(self.edit_selected_client)

        self.delete_button = QPushButton('Удалить клиента', self)
        self.delete_button.clicked.connect(self.delete_selected_client)

        self.sort_last_name_button = QPushButton('Сортировать по фамилии', self)
        self.sort_last_name_button.clicked.connect(lambda: self.controller.sort_clients('LastName'))

        self.sort_phone_button = QPushButton('Сортировать по номеру', self)
        self.sort_phone_button.clicked.connect(lambda: self.controller.sort_clients('Phone'))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.sort_last_name_button)
        button_layout.addWidget(self.sort_phone_button)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_table(self, clients=None):
        if clients is None:
            clients = self.controller.repository.get_clients()
        self.table.setRowCount(len(clients))
        for i, client in enumerate(clients):
            self.table.setItem(i, 0, QTableWidgetItem(client.LastName))
            self.table.setItem(i, 1, QTableWidgetItem(client.FirstName))
            self.table.setItem(i, 2, QTableWidgetItem(client.MiddleName))
            self.table.setItem(i, 3, QTableWidgetItem(client.Address))
            self.table.setItem(i, 4, QTableWidgetItem(client.Phone))

    def edit_selected_client(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.controller.show_edit_client_dialog(selected_row)
        else:
            QMessageBox.warning(self, 'Клиент не выбран', 'Выберите клиента для изменения')

    def delete_selected_client(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.controller.delete_client(selected_row)
        else:
            QMessageBox.warning(self, 'Клиент не выбран', 'Выберите клиента для удаления')

class ClientFormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить клиента')
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

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

    def get_client_data(self):
        return {
            'LastName': self.last_name.text(),
            'FirstName': self.first_name.text(),
            'MiddleName': self.middle_name.text(),
            'Address': self.address.text(),
            'Phone': self.phone.text()
        }

class EditClientDialog(QDialog):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client = client
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Изменить клиента')
        self.layout = QFormLayout(self)

        self.last_name = QLineEdit(self.client.LastName, self)
        self.first_name = QLineEdit(self.client.FirstName, self)
        self.middle_name = QLineEdit(self.client.MiddleName, self)
        self.address = QLineEdit(self.client.Address, self)
        self.phone = QLineEdit(self.client.Phone, self)

        self.layout.addRow('Last Name', self.last_name)
        self.layout.addRow('First Name', self.first_name)
        self.layout.addRow('Middle Name', self.middle_name)
        self.layout.addRow('Address', self.address)
        self.layout.addRow('Phone', self.phone)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

    def get_client_data(self):
        return {
            'LastName': self.last_name.text(),
            'FirstName': self.first_name.text(),
            'MiddleName': self.middle_name.text(),
            'Address': self.address.text(),
            'Phone': self.phone.text()
        }