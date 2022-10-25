from PyQt5.QtWidgets import QMessageBox


def info_ok_box(text, name="Info"):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle(name)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()
