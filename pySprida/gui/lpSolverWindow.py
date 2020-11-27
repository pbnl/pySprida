from PyQt5.QtWidgets import QMainWindow

from pySprida.data.dataContainer import DataContainer
from pySprida.gui.lpsolveredit import Ui_LPSolverEdit


class LPSolverWindow(QMainWindow):

    def __init__(self, container: DataContainer, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_LPSolverEdit()
        self.ui.setupUi(self)
        self.container = container
        config = container.solver_config["lp"]
        self.ui.max_time.setText(str(config["max_time"]))
        self.ui.equal_lesson_weight.setText(str(config["equal_lesson_weight"]))
        self.ui.equal_subject_weight.setText(str(config["equal_subject_weight"]))

        self.ui.max_time.textChanged.connect(self.max_time_change)
        self.ui.equal_lesson_weight.textChanged.connect(self.equal_lesson_weight_change)
        self.ui.equal_subject_weight.textChanged.connect(self.equal_subject_weighte_change)

    def max_time_change(self):
        if self.ui.max_time.text() == "":
            self.container.solver_config["lp"]["max_time"] = 0
            return
        self.container.solver_config["lp"]["max_time"] = float(self.ui.max_time.text())

    def equal_lesson_weight_change(self):
        if self.ui.equal_lesson_weight.text() == "":
            self.container.solver_config["lp"]["equal_lesson_weight"] = 0
            return
        self.container.solver_config["lp"]["equal_lesson_weight"] = float(self.ui.equal_lesson_weight.text())

    def equal_subject_weighte_change(self):
        if self.ui.equal_subject_weight.text() == "":
            self.container.solver_config["lp"]["equal_subject_weight"] = 0
            return
        self.container.solver_config["lp"]["equal_subject_weight"] = float(self.ui.equal_subject_weight.text())
