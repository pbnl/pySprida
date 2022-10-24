from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtWidgets
from pySprida.data.dataContainer import DataContainer
from pySprida.gui.lpsolveredit import Ui_LPSolverEdit
from pySprida.utils import info_ok_box


class LPSolverWindow(QMainWindow):

    def __init__(self, container: DataContainer, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_LPSolverEdit()
        self.ui.setupUi(self)
        self.container = container
        config = container.solver_config["lp"]
        self.ui.max_time.setText(str(config["max_time"]))
        self.ui.equal_lesson_weight.setText(str(config["equal_lesson_weight"]))
        self.ui.equal_subject_weight.setText(
            str(config["equal_subject_weight"]))

        self.ui.max_time.textChanged.connect(self.max_time_change)
        self.ui.equal_lesson_weight.textChanged.connect(
            self.equal_lesson_weight_change)
        self.ui.equal_subject_weight.textChanged.connect(
            self.equal_subject_weighte_change)

        self.set_max_groups_per_groupType_table()
        self.ui.max_different_groups_per_groupType.itemChanged.connect(self.update_max_groups_per_groupType)

    def max_time_change(self):
        if self.ui.max_time.text() == "":
            self.container.solver_config["lp"]["max_time"] = 0
            return
        self.container.solver_config["lp"]["max_time"] = float(
            self.ui.max_time.text())

    def equal_lesson_weight_change(self):
        if self.ui.equal_lesson_weight.text() == "":
            self.container.solver_config["lp"]["equal_lesson_weight"] = 0
            return
        self.container.solver_config["lp"]["equal_lesson_weight"] = float(
            self.ui.equal_lesson_weight.text())

    def equal_subject_weighte_change(self):
        if self.ui.equal_subject_weight.text() == "":
            self.container.solver_config["lp"]["equal_subject_weight"] = 0
            return
        self.container.solver_config["lp"]["equal_subject_weight"] = float(
            self.ui.equal_subject_weight.text())


    def update_max_groups_per_groupType(self, item):
        if item.row() == 0:
            value = self.ui.max_different_groups_per_groupType.item(0, item.column()).text()
            group_type = self.container.group_type_names[item.column()]
            groups_of_type = self.container.get_num_groups_per_type()
            if value.isnumeric():
                if int(value) >= 1 and int(value) <= groups_of_type[group_type]:
                    if "max_groups_per_groupType" not in self.container.solver_config["lp"]:
                        self.container.solver_config["lp"]["max_groups_per_groupType"] = {}
                    self.container.solver_config["lp"]["max_groups_per_groupType"][group_type] = int(value)
                else:
                    info_ok_box('Use only integers and values between one and the number of groups in this type')

    def set_max_groups_per_groupType_table(self):
        group_type_names = self.container.group_type_names
        max_different = self.container.solver_config["lp"].get("max_groups_per_groupType", {})
        groups_of_type = self.container.get_num_groups_per_type()
        self.ui.max_different_groups_per_groupType.setRowCount(1)
        self.ui.max_different_groups_per_groupType.setColumnCount(len(group_type_names))
        for n, gtype in enumerate(group_type_names):
            newitem = QTableWidgetItem(str(max_different.get(gtype, groups_of_type[gtype])))
            self.ui.max_different_groups_per_groupType.setItem(0, n, newitem)
            self.ui.max_different_groups_per_groupType.setColumnWidth(n, 10)
        self.ui.max_different_groups_per_groupType.setHorizontalHeaderLabels(group_type_names)
