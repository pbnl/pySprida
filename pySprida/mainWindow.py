import json
from pathlib import Path

import xlsxwriter
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys

from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from mip import OptimizationStatus

from pySprida.data.dataContainer import DataContainer
from pySprida.data.lpData import LPData
from pySprida.gui.lpSolverWindow import LPSolverWindow
from pySprida.gui.main import Ui_MainWindow
from pySprida.gui.solution_window import SolutionWindow
from pySprida.solver.lpSolver import LPSolver


def info_ok_box(text, name="Info"):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle(name)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, primary_screen, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.primary_screen = primary_screen

        self.ui.config_path_select_button.clicked.connect(self.select_config_file)
        self.ui.load_config_button.clicked.connect(self.load_config)
        self.ui.generate_button.clicked.connect(self.generate)
        self.ui.solver_edit_button.clicked.connect(self.open_solver_edit_window)
        self.ui.save_problem_button.clicked.connect(self.save_problem)
        self.ui.export_solution_button.clicked.connect(self.export_solution)

        self.container = None
        self.solution = None
        # self.load_debug_data()

    def export_solution(self):
        if self.solution is None:
            info_ok_box("Generate a solution first")
            return
        name = QFileDialog.getSaveFileName(
            self,
            'Save File',
            "/home/pauli/Dokumente/Pfadfinder/Schulung_neu/Schulungen/21/Stunde- und Raumplan/erste Pläne vom 12.04/",
            "*.xlsx")[0]
        workbook = xlsxwriter.Workbook(name)
        worksheet = workbook.add_worksheet()
        mapping_matrix = self.solution.get_mapping_matrix()
        subject_names = self.container.get_subject_names()
        gtypes_names = self.container.get_group_names()
        for i, sub_name in enumerate(subject_names):
            worksheet.write(0, 1 + i * len(gtypes_names), sub_name)
            for j, gname in enumerate(gtypes_names):
                worksheet.write(1, 1 + i * len(gtypes_names) + j, gname)
        worksheet.set_column(1, len(subject_names) * len(gtypes_names) + 1, 3)
        for i, teacher in enumerate(self.container.teachers):
            worksheet.write(i + 2, 0, teacher.name)
            for j, selected in enumerate(mapping_matrix[i]):
                if selected:
                    worksheet.write(i + 2, j + 1, "x")
                else:
                    worksheet.write(i + 2, j + 1, "")
        workbook.close()

    def save_problem(self):
        if self.container is None:
            info_ok_box("Load some data first")
            return
        json_data = self.container.to_json()
        name = QFileDialog.getSaveFileName(self, 'Save File', "a_name.json", "*.json")[0]
        if name:
            with open(name, 'w', encoding="UTF-8") as f:
                json.dump(json_data, f, indent=4, sort_keys=True, ensure_ascii=False)

    def select_config_file(self):
        data_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open File', r"/home/pauli/Dokumente/Pfadfinder/Schulung_neu/Schulungen/21/Stunde- und Raumplan/erste Pläne vom 12.04/", '*.json')
        self.ui.config_path.setText(data_path)

    def load_config(self):
        path = self.ui.config_path.text()
        self.container = DataContainer()
        try:
            self.container.load_data(Path(path))
        except (IsADirectoryError, FileNotFoundError):
            info_ok_box(f"File {str(path)} was not found!")
        self.load_preview_data()

    def load_preview_data(self):
        self.ui.teacher_list.clear()
        self.ui.subject_list.clear()
        self.ui.groups_list.clear()
        for teacher in self.container.teachers:
            self.ui.teacher_list.addItem(teacher.name)
        for group in self.container.groups:
            self.ui.groups_list.addItem(group.name)
        for subject_type in self.container.subject_types:
            self.ui.subject_list.addItem(subject_type.name)

    def generate(self):
        if self.container is None:
            info_ok_box("Load some data first")
            return
        solver = self.ui.solver_selector.currentText()
        if solver == "LP":
            problem = LPData(self.container)
            self.solver = LPSolver(problem, self.container)
            self.solver.finished.connect(self.show_solution)
            self.solver.start()
            self.ui.generate_button.setText("Working")
            self.ui.generate_button.setDisabled(True)
            self.ui.status.setText("Working")
        else:
            info_ok_box(f"No solver with the name: {str(solver)}")
            raise Exception("Wrong solver")

    def show_solution(self, solution):
        self.ui.generate_button.setText("Generate")
        self.ui.generate_button.setDisabled(False)
        self.ui.status.setText("Finished")
        self.ui.solution_type.setText(solution.status_name)

        if solution.relaxed_loss:
            self.ui.loss_progress.setMaximum(solution.relaxed_loss)
            self.ui.ub_value.setText(str(solution.relaxed_loss))
        if solution.loss:
            self.ui.loss_progress.setValue(solution.loss)
            self.ui.solution_value.setText(str(solution.loss))
        if solution.status == OptimizationStatus.FEASIBLE or solution.status == OptimizationStatus.OPTIMAL:
            self.solution = solution
            self.solution_window = SolutionWindow(solution, self.container)
            self.solution_window.show()
        else:
            self.ui.ub_value.setText("-")
            self.ui.solution_value.setText("-")
            self.ui.loss_progress.setValue(0)

    def set_solver_status(self):
        print("Test")

    def load_debug_data(self):
        self.ui.config_path.setText(r"/home/paul/PycharmProjects/pySprida/testData/csv_config2021.json")
        self.load_config()

    def open_solver_edit_window(self):
        if self.container is None:
            info_ok_box("Load some data first")
            return
        self.lp_edit_window = LPSolverWindow(self.container)
        self.lp_edit_window.show()
