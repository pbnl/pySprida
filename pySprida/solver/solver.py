from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread

from pySprida.data.solution import Solution


class Solver(QThread):

    finished = pyqtSignal(Solution)

    def __init__(self, problem, data_container):
        super().__init__()
        self.problem = problem
        self.data_container = data_container

    def solve(self) -> Solution:
        pass

    def run(self):
        solution = self.solve()
        self.finished.emit(solution)
