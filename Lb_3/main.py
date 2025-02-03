import sys
from PyQt5.QtWidgets import QApplication
from client_controller import ClientController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = ClientController()
    controller.run()
    sys.exit(app.exec_())
