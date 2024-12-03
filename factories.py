from views import ItemFormView
from controllers import MainController, AddItemController, EditItemController


class ControllerFactory:
    @staticmethod
    def create_add_item_controller(repo):
        """Создает контроллер для добавления нового элемента."""
        view = ItemFormView()
        return AddItemController(view, repo)

    @staticmethod
    def create_edit_item_controller(repo, item):
        """Создает контроллер для редактирования существующего элемента."""
        view = ItemFormView(item)
        return EditItemController(view, repo, item)


class MainControllerFactory:
    @staticmethod
    def create(repo):
        """Создает основной контроллер для приложения."""
        from views import MainView
        view = MainView()
        return MainController(view, repo)
