from PyQt5.QtWidgets import QInputDialog, QMessageBox
from models import Item

class MainController:
    def __init__(self, view, repository):
        self.view = view
        self.repo = repository

        # Подключаем сигналы
        self.view.add_button.clicked.connect(self.add_item)
        self.view.edit_button.clicked.connect(self.edit_item)
        self.view.delete_button.clicked.connect(self.delete_item)

        # Инициализируем таблицу
        self.refresh_table()

    def refresh_table(self):
        items = self.repo.get_all_items()
        self.view.update_table(items)

    def add_item(self):
        id, ok1 = QInputDialog.getInt(self.view, "Добавить товар", "Введите ID:")
        if not ok1:
            return
        name, ok2 = QInputDialog.getText(self.view, "Добавить товар", "Введите название:")
        if not ok2:
            return
        price, ok3 = QInputDialog.getDouble(self.view, "Добавить товар", "Введите цену:")
        if not ok3:
            return

        self.repo.add_item(Item(id, name, price))
        self.refresh_table()

    def edit_item(self):
        selected_row = self.view.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.view, "Ошибка", "Выберите строку для редактирования.")
            return

        id = int(self.view.table.item(selected_row, 0).text())
        item = next((i for i in self.repo.get_all_items() if i.id == id), None)

        if not item:
            QMessageBox.warning(self.view, "Ошибка", "Не удалось найти товар.")
            return

        name, ok1 = QInputDialog.getText(self.view, "Редактировать товар", "Введите новое название:", text=item.name)
        if not ok1:
            return
        price, ok2 = QInputDialog.getDouble(self.view, "Редактировать товар", "Введите новую цену:", value=item.price)
        if not ok2:
            return

        self.repo.update_item(id, Item(id, name, price))
        self.refresh_table()

    def delete_item(self):
        selected_row = self.view.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.view, "Ошибка", "Выберите строку для удаления.")
            return

        id = int(self.view.table.item(selected_row, 0).text())
        self.repo.delete_item(id)
        self.refresh_table()
