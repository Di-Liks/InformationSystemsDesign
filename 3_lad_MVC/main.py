import sys
from PyQt5.QtWidgets import QApplication
from models import Repository, FilteredRepository
from factories import MainControllerFactory


def main():
    app = QApplication(sys.argv)
    repo = FilteredRepository(Repository())
    controller = MainControllerFactory.create(repo)
    controller.view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
