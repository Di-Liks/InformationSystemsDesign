from PyQt5.QtWidgets import QApplication
from models import Repository
from views import MainView
from controllers import MainController


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    repo = Repository("data.json")
    view = MainView()
    controller = MainController(view, repo)

    view.show()
    sys.exit(app.exec_())
