from views import ItemFormView
from controllers import AddItemController, EditItemController


class ControllerFactory:
    @staticmethod
    def create_add_item_controller(repo):
        view = ItemFormView()
        return AddItemController(view, repo)

    @staticmethod
    def create_edit_item_controller(repo, item):
        view = ItemFormView(item)
        return EditItemController(view, repo)
