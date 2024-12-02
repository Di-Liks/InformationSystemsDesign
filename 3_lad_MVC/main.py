import sys
from PyQt5.QtWidgets import QApplication
from models import Repository, Item
from views import MainView
from controllers import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем репозиторий с начальными данными
    repo = Repository()
    repo.add_item(Item(1, "Товар 1", 10.99))
    repo.add_item(Item(2, "Товар 2", 25.50))
    repo.add_item(Item(3, "Товар 3", 5.99))

    # Создаем представление и контроллер
    view = MainView()
    controller = MainController(view, repo)

    # Показываем главное окно
    view.show()
    sys.exit(app.exec_())
