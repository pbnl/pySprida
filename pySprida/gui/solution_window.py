import logging
import sys
from pathlib import Path
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QBrush
from PyQt5.QtWidgets import QTableView, QDesktopWidget, QStyledItemDelegate, QStyle, QWidget, QMainWindow

from pySprida.data.dataContainer import DataContainer
from pySprida.data.solution import Solution


class ColoredMappingTableModel(QtCore.QAbstractTableModel):
    def __init__(self, solution: Solution, data_container: DataContainer):
        super(ColoredMappingTableModel, self).__init__()
        self.data_container = data_container
        self._mapping = solution.get_mapping_matrix()
        self._preferences = self.data_container.updated_pref
        self._teacher_names = data_container.get_teacher_names()
        self._group_names = data_container.get_group_names()
        self._subject_names = data_container.get_subject_names()
        self._num_lessons = solution.get_teacher_num_lessons()
        self._co_ref = data_container.get_teacher_co_ref()

    def update_pref(self, row, col, pref):
        self._preferences[row][col] = pref
        self.data_container.updated_pref = self._preferences

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            if index.row() == 0:
                if index.column() == 0:
                    return "Num"
                else:
                    return self._subject_names[(index.column() - 1) // len(self._group_names)]
            elif index.row() == 1:
                if index.column() > 0:
                    return self._group_names[(index.column() - 1) % len(self._group_names)]
            else:
                if index.column() == 0:
                    return str(self._num_lessons[index.row() - 2])
                elif self._mapping[index.row() - 2][index.column() - 1]:
                    return "X"
            return ""
        if role == Qt.BackgroundRole:
            second_col = ((index.column() - 1) // len(self._group_names)) % 2
            if index.row() == 1:
                if second_col:
                    return QtGui.QColor("#9da1fc")
                else:
                    return QtGui.QColor("#bdc0ff")
            if index.row() > 1:
                if index.column() == 0:
                    if self._co_ref[index.row() - 2]:
                        return QtGui.QColor("#348feb")
                    else:
                        return QtGui.QColor("#ffffff")
                value = self._preferences[index.row() - 2][index.column() - 1]
                if value == 0:
                    return QtGui.QColor("#ffffff")
                elif value >= 1 and value <= 2:
                    if second_col:
                        return QtGui.QColor("#d95f5f")
                    else:
                        return QtGui.QColor("#ff7070")
                elif value == 6:
                    if second_col:
                        return QtGui.QColor("#f542ef")
                    else:
                        return QtGui.QColor("#9e289a")
                elif value == 0:
                    if second_col:
                        return QtGui.QColor("#d95f5f")
                    else:
                        return QtGui.QColor("#ff7070")
                elif value == -1:
                    if second_col:
                        return QtGui.QColor("#000000")
                    else:
                        return QtGui.QColor("#000000")
                elif value == 3:
                    if second_col:
                        return QtGui.QColor("#d4c23d")
                    else:
                        return QtGui.QColor("#ffea4a")
                else:
                    if second_col:
                        return QtGui.QColor("#6fcf3c")
                    else:
                        return QtGui.QColor("#89ff4a")

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._mapping) + 2

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._mapping[0]) + 1

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            # if orientation == Qt.Horizontal:
            #    return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                if section == 0:
                    return "Type"
                elif section == 1:
                    return "Kurs"
                else:
                    return str(self._teacher_names[section - 2])


class StyleDelegateForQTableWidget(QStyledItemDelegate):
    color_default = QColor("#aaedff")

    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            option.palette.setColor(QPalette.HighlightedText, Qt.black)
            color = self.combineColors(self.color_default, self.background(option, index))
            option.palette.setColor(QPalette.Highlight, color)
        QStyledItemDelegate.paint(self, painter, option, index)

    def background(self, option, index):
        color = self.parent().model().data(index, Qt.BackgroundRole)
        return color

    @staticmethod
    def combineColors(c1, c2):
        c3 = QColor()
        c3.setRed((c1.red() + c2.red()) / 2)
        c3.setGreen((c1.green() + c2.green()) / 2)
        c3.setBlue((c1.blue() + c2.blue()) / 2)

        return c3


class ColoredMappingTableView(QTableView):
    adjusted_pref = pyqtSignal(int, int, int)

    def __init__(self, data_container: DataContainer):
        super().__init__()
        # We need this to allow navigating without editing
        self.catch = False

        self._data_container = data_container
        self._num_groups = data_container.num_groups
        self._num_courses = data_container.num_cources
        self._num_teachers = data_container.num_teacher
        for i in range(0, self._num_courses // self._num_groups):
            self.setSpan(0, i * self._num_groups + 1, 1, self._num_groups)

        self.setItemDelegate(StyleDelegateForQTableWidget(self))

        self.keys = [Qt.Key_1,
                     Qt.Key_2,
                     Qt.Key_3,
                     Qt.Key_4,
                     Qt.Key_5,
                     Qt.Key_R,
                     Qt.Key_N,
                     Qt.Key_Y]

    def ajust_size(self):
        self.setRowHeight(0, 1)
        self.setColumnWidth(0, 1)
        for i in range(self._num_courses):
            self.setColumnWidth(i + 1, 1)
        for i in range(self._num_teachers + 2):
            self.setRowHeight(i + 1, 1)

    def focusInEvent(self, event):
        self.catch = False
        return QTableView.focusInEvent(self, event)

    def focusOutEvent(self, event):
        self.catch = True
        return QTableView.focusOutEvent(self, event)

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in self.keys:
            self.adjust_pref(event.key())

        return QTableView.event(self, event)

    def adjust_pref(self, key):
        if key == Qt.Key_N:
            pref = -1
        elif key == Qt.Key_Y:
            pref = 6
        else:
            pref = self.keys.index(key) + 1
        selected = self.selectedIndexes()[0]
        row = selected.row()
        col = selected.column()

        self.model().update_pref(row - 2, col - 1, pref)
        self.update()
        self.adjusted_pref.emit(row - 2, col - 1, pref)


class SolutionWindow(QMainWindow):
    def __init__(self, solution, dataContainer):
        super().__init__()

        self.table = ColoredMappingTableView(dataContainer)
        self.model = ColoredMappingTableModel(solution, dataContainer)
        self.table.setModel(self.model)
        self.table.ajust_size()

        self.setCentralWidget(self.table)

        #dw = QDesktopWidget()
        #x = int(dw.width() * 0.7)
        #y = int(dw.height() * 0.7)
        #self.resize(x, y)
        self.adjustSize()
        self.setWindowTitle("PySprida-Solution")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/testProblem.json"))
    printer.printTeachers(container)
    printer.printGroups(container)

    app = QtWidgets.QApplication(sys.argv)
    window = SolutionWindow(Solution(np.random.randint(0, 2, (15 * 11 * 3)), container), container)
    window.show()
    app.exec_()
