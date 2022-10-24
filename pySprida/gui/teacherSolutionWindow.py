from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from pySprida.data.dataContainer import DataContainer
from pySprida.gui.lpsolveredit import Ui_LPSolverEdit
from pySprida.gui.teacherSolution import Ui_TeacherSolution


class TeacherSolutionWindow(QMainWindow):

    def __init__(self, container: DataContainer, teacher_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_TeacherSolution()
        self.ui.setupUi(self)
        self.container = container
        self.teacher_id = teacher_id
        self.update_selected_groups()

    def update_selected_groups(self):
        group_names = self.container.get_group_names()
        selected_groups = self.container.last_solution.getSelectedGroups(self.teacher_id)
        self.ui.selected_groups.setRowCount(1)
        self.ui.selected_groups.setColumnCount(len(group_names))
        for n, key in enumerate(selected_groups):
            if key == 0:
                newitem = QTableWidgetItem("")
            if key == 1:
                newitem = QTableWidgetItem("x")
            self.ui.selected_groups.setItem(0, n, newitem)
            self.ui.selected_groups.setColumnWidth(n, 10)
        self.ui.selected_groups.setHorizontalHeaderLabels(group_names)
