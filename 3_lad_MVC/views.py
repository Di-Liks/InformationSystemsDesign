from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Товары")
        self.resize(600, 400)

        # Главный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Цена"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Кнопки
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        central_widget.setLayout(layout)

    def update_table(self, items):
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(row, 1, QTableWidgetItem(item.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.price)))
