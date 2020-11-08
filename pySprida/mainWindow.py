from pathlib import Path

from PyQt5 import QtWidgets, uic, QtCore
import sys

from pySprida.data.dataContainer import DataContainer
from pySprida.data.lpData import LPData
from pySprida.gui.main import Ui_MainWindow
from pySprida.gui.solution_window import SolutionWindow
from pySprida.solver.lpSolver import LPSolver


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.config_path_select_button.clicked.connect(self.select_config_file)
        self.ui.load_config_button.clicked.connect(self.load_config)
        self.ui.generate_button.clicked.connect(self.generate)

        self.load_debug_data()


    def select_config_file(self):
        data_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', r"/home/paul/PycharmProjects/pySprida/testData", '*.json')
        self.ui.config_path.setText(data_path)

    def load_config(self):
        path = self.ui.config_path.text()
        self.container = DataContainer()
        self.container.load_data(Path(path))

    def generate(self):
        solver = self.ui.solver_selector.currentText()
        if solver == "LP":
            problem = LPData(self.container)
            solver = LPSolver(problem, self.container, max_time=2)
            solver.finished.connect(self.show_solution)
            solver.start()
            self.ui.generate_button.setText("Working")
            self.ui.generate_button.setDisabled(True)
            self.ui.status.setText("Working")
        else:
            raise Exception("Wrong solver")

    def show_solution(self, solution):
        self.ui.generate_button.setText("Generate")
        self.ui.generate_button.setDisabled(False)
        self.ui.status.setText("Finished")
        self.ui.solution_type.setText(solution.status_name)
        self.ui.solution_value.setText(str(solution.loss))
        self.ui.ub_value.setText(str(solution.relaxed_loss))

        self.ui.loss_progress.setMaximum(solution.relaxed_loss)
        self.ui.loss_progress.setValue(solution.loss)

        self.solution_window = SolutionWindow(solution, self.container)
        self.solution_window.show()

    def set_solver_status(self):
        print("Test")

    def load_debug_data(self):
        self.ui.config_path.setText(r"/home/paul/PycharmProjects/pySprida/testData/csv_config2021.json")
        self.load_config()
        self.generate()
