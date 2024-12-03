from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QDialog, QFormLayout, QDialogButtonBox
)


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

        self.filter_button = QPushButton("Применить фильтр")
        self.layout.addWidget(self.filter_button)

        self.reset_filter_button = QPushButton("Сбросить фильтр")
        self.layout.addWidget(self.reset_filter_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def update(self, items):
        self.table.setRowCount(len(items))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Цена"])

        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(row, 1, QTableWidgetItem(item.name))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item.price:.2f}"))


class ItemFormView(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.setWindowTitle("Форма")
        self.layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()

        if item:
            self.id_input.setText(str(item.id))
            self.name_input.setText(item.name)
            self.price_input.setText(str(item.price))

        self.layout.addRow(QLabel("ID:"), self.id_input)
        self.layout.addRow(QLabel("Название:"), self.name_input)
        self.layout.addRow(QLabel("Цена:"), self.price_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)
