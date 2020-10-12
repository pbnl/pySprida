import logging
import sys
from pathlib import Path
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableView

from pySprida.data.dataContainer import DataContainer
from pySprida.data.solution import Solution


class ColoredMappingTableModel(QtCore.QAbstractTableModel):
    def __init__(self, solution: Solution, data_container: DataContainer):
        super(ColoredMappingTableModel, self).__init__()
        self._mapping = solution.get_mapping_matrix()
        self._preferences = data_container.get_preference_matrix()
        self._teacher_names = data_container.get_teacher_names()
        self._group_names = data_container.get_group_names()
        self._subject_names = data_container.get_subject_names()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            if index.row() == 0:
                return self._subject_names[index.column() // len(self._group_names)]
            elif index.row() == 1:
                return self._group_names[index.column() % len(self._group_names)]
            else:
                if self._mapping[index.row() - 2][index.column()]:
                    return "X"
            return ""
        if role == Qt.BackgroundRole:
            second_col = (index.column() // len(self._group_names)) % 2
            if index.row() == 1:
                if second_col:
                    return QtGui.QColor("#9da1fc")
                else:
                    return QtGui.QColor("#bdc0ff")
            if index.row() > 1:
                value = self._preferences[index.row() - 2][index.column()]
                if value == 0:
                    return QtGui.QColor("#ffffff")
                elif value >= 1 and value <= 2:
                    if second_col:
                        return QtGui.QColor("#d95f5f")
                    else:
                        return QtGui.QColor("#ff7070")
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
        return len(self._mapping[0])

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


class ColoredMappingTableView(QTableView):
    def __init__(self, data_container: DataContainer):
        super().__init__()
        self._data_container = data_container
        self._num_groups = data_container.num_groups
        self._num_courses = data_container.num_cources
        self._num_teachers = data_container.num_teacher
        for i in range(self._num_courses // self._num_groups):
            self.setSpan(0, i * self._num_groups, 1, self._num_groups)

    def ajust_size(self):
        for i in range(self._num_courses):
            self.setColumnWidth(i, 1)
        for i in range(self._num_teachers + 2):
            self.setRowHeight(i, 1)


class SolutionWindow(QtWidgets.QMainWindow):
    def __init__(self, solution, dataContainer):
        super().__init__()

        self.table = ColoredMappingTableView(dataContainer)
        self.model = ColoredMappingTableModel(solution, dataContainer)
        self.table.setModel(self.model)
        self.table.ajust_size()

        self.setCentralWidget(self.table)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/testProblem.json"))
    printer.printTeachers(container)
    printer.printGroups(container)

    app = QtWidgets.QApplication(sys.argv)
    window = SolutionWindow(Solution(np.random.randint(0, 2, (18 * 10 * 3)), container), container)
    window.show()
    app.exec_()
