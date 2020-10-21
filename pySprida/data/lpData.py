import logging
from pathlib import Path

from pySprida.data.dataContainer import DataContainer
import numpy as np


class LPData:

    def __init__(self, data_container: DataContainer):
        self._data_container = data_container

    def get_preferences(self):
        preferences = np.zeros(0)
        for teacher in self._data_container.teachers:
            teacher_prefs = np.array(teacher.preferences).reshape(-1)
            preferences = np.append(preferences, teacher_prefs)
        return preferences

    def get_max_time(self):
        max_lessons = np.zeros(0)
        for teacher in self._data_container.teachers:
            max_lessons = np.append(max_lessons, teacher.max_lessons)
        return max_lessons


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/testProblem.json"))
    lpData = LPData(container)
    lpData.get_preferences()
