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
            teacher_prefs = teacher.get_all_subject_preferences()
            teacher_prefs = teacher_prefs.reshape(-1)
            preferences = np.append(preferences, teacher_prefs)
        return preferences

    def get_max_time(self):
        max_lessons = np.zeros(0)
        for teacher in self._data_container.teachers:
            max_lessons = np.append(max_lessons, teacher.max_lessons)
        return max_lessons

    def get_num_teche(self):
        return len(self._data_container.teachers)

    def get_num_groups(self):
        return len(self._data_container.groups)

    def get_num_subjects(self):
        return len(self._data_container.subject_types)

    def lesson_exist_list(self):
        existing = []
        for group in self._data_container.groups:
            type = group.group_type
            for subject in type.existing_noneexisting_subjects:
                if subject:
                    existing.append(True)
                else:
                    existing.append(False)
        existing = np.array(existing).reshape(self._data_container.num_groups, self._data_container.num_subjects)
        existing = np.transpose(existing)
        existing = existing.reshape(-1)
        return existing

    def get_lessons_per_subject(self):
        lessons = []
        for group in self._data_container.groups:
            type = group.group_type
            for subject in type.existing_noneexisting_subjects:
                if subject is None:
                    lessons.append(0)
                else:
                    lessons.append(subject.num_lessons)
        lessons = np.array(lessons).reshape(self._data_container.num_groups, self._data_container.num_subjects)
        lessons = np.transpose(lessons)
        lessons = lessons.reshape(-1)
        return lessons


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/testProblem.json"))
    lpData = LPData(container)
    lpData.get_preferences()
