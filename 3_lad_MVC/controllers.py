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

        self.update_view()

    def update_view(self):
        self.view.update(self.repo.get_all_items())

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


class AddItemController:
    def __init__(self, view, repo):
        self.view = view
        self.repo = repo
        self.view.submit_button.clicked.connect(self.add_item)

    def add_item(self):
        name, price = self.view.get_data()
        if not name or not price.isdigit():
            QMessageBox.warning(self.view, "Ошибка", "Введите корректные данные.")
            return

        item = Item(id=len(self.repo.get_all_items()) + 1, name=name, price=float(price))
        self.repo.add_item(item)
        self.view.close()


class EditItemController:
    def __init__(self, view, repo, item):
        self.view = view
        self.repo = repo
        self.item = item
        self.view.submit_button.clicked.connect(self.edit_item)

    def edit_item(self):
        name, price = self.view.get_data()
        if not name or not price.isdigit():
            QMessageBox.warning(self.view, "Ошибка", "Введите корректные данные.")
            return

        updated_item = Item(id=self.item.id, name=name, price=float(price))
        self.repo.update_item(self.item.id, updated_item)
        self.view.close()
