from PyQt5.QtWidgets import QMessageBox
from models import Item


class MainController:
    def __init__(self, view, repo):
        self.view = view
        self.repo = repo

        self.repo.add_observer(self.view)

        self.view.add_button.clicked.connect(self.add_item)
        self.view.edit_button.clicked.connect(self.edit_item)
        self.view.delete_button.clicked.connect(self.delete_item)
        self.view.filter_button.clicked.connect(self.apply_filter)
        self.view.reset_filter_button.clicked.connect(self.reset_filter)

        self.update_view()

    def update_view(self):
        self.view.update(self.repo.get_filtered_items())

    def add_item(self):
        from factories import ControllerFactory
        controller = ControllerFactory.create_add_item_controller(self.repo)
        controller.view.exec_()
        self.update_view()

    def edit_item(self):
        selected_row = self.view.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.view, "Ошибка", "Выберите запись для редактирования.")
            return

        item_id = int(self.view.table.item(selected_row, 0).text())
        item = next((i for i in self.repo.get_all_items() if i.id == item_id), None)

        from factories import ControllerFactory
        controller = ControllerFactory.create_edit_item_controller(self.repo, item)
        controller.view.exec_()
        self.update_view()

    def delete_item(self):
        selected_row = self.view.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.view, "Ошибка", "Выберите запись для удаления.")
            return

        item_id = int(self.view.table.item(selected_row, 0).text())
        self.repo.delete_item(item_id)
        self.update_view()

    def apply_filter(self):
        from PyQt5.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self.view, "Фильтр", "Введите минимальную цену:")
        if ok:
            try:
                min_price = float(text)
                self.repo.set_filter(lambda item: item.price >= min_price)
                self.update_view()
            except ValueError:
                QMessageBox.warning(self.view, "Ошибка", "Введите корректное число.")

    def reset_filter(self):
        self.repo.set_filter(None)
        self.update_view()


class AddItemController:
    def __init__(self, view, repo):
        self.view = view
        self.repo = repo

        self.view.buttons.accepted.connect(self.add_item)
        self.view.buttons.rejected.connect(self.view.reject)

    def add_item(self):
        try:
            id = int(self.view.id_input.text())
            name = self.view.name_input.text()
            price = float(self.view.price_input.text())
            self.repo.add_item(Item(id, name, price))
            self.view.accept()
        except ValueError:
            QMessageBox.warning(self.view, "Ошибка", "Введите корректные данные.")


class EditItemController:
    def __init__(self, view, repo, item):
        self.view = view
        self.repo = repo
        self.item = item

        self.view.buttons.accepted.connect(self.save_item)
        self.view.buttons.rejected.connect(self.view.reject)

    def save_item(self):
        try:
            new_id = int(self.view.id_input.text())
            new_name = self.view.name_input.text()
            new_price = float(self.view.price_input.text())
            new_item = Item(new_id, new_name, new_price)
            self.repo.update_item(self.item.id, new_item)
            self.view.accept()
        except ValueError:
            QMessageBox.warning(self.view, "Ошибка", "Введите корректные данные.")
