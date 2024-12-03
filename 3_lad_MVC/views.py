from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QLineEdit, QLabel


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD-приложение")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.add_button = QPushButton("Добавить запись")
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Редактировать запись")
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить запись")
        self.layout.addWidget(self.delete_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def update(self, items):
        self.table.setRowCount(len(items))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Цена"])

        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(row, 1, QTableWidgetItem(item.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.price)))


class ItemFormView(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.setWindowTitle("Добавить/Редактировать запись")
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.price_input = QLineEdit()

        if item:
            self.name_input.setText(item.name)
            self.price_input.setText(str(item.price))

        self.layout.addWidget(QLabel("Название"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Цена"))
        self.layout.addWidget(self.price_input)

        self.submit_button = QPushButton("Сохранить")
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_data(self):
        return self.name_input.text(), self.price_input.text()
