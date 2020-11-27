from PyQt5 import QtWidgets, uic
import sys

from pySprida.mainWindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(app.primaryScreen())
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
