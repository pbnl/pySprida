import logging
import sys
from pathlib import Path
from PyQt5 import QtWidgets

from pySprida.data.dataContainer import DataContainer
from pySprida.data.lpData import LPData
from pySprida.gui.solution_window import SolutionWindow
from pySprida.solver.lpSolver import LPSolver

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/csv_config2021.json"))
    printer.printTeachers(container)
    printer.printGroups(container)

    problem = LPData(container)
    solver = LPSolver(problem, container)
    solution = solver.solve()

    app = QtWidgets.QApplication(sys.argv)
    window = SolutionWindow(solution, container)
    window.show()
    app.exec_()