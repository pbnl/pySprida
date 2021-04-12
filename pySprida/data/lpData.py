import logging
from pathlib import Path

from pySprida.data.dataContainer import DataContainer
import numpy as np


class LPData:

    def __init__(self, data_container: DataContainer):
        self._data_container = data_container
        self.config = data_container.solver_config["lp"]
        self.weight_adjustments = self.config["weight_adjustments"]

    def get_preferences(self):
        preferences = self._data_container.updated_pref.reshape(-1)
        preferences_adjustet_weights = preferences
        for weight, adjusted_weight in self.weight_adjustments.items():
            preferences_adjustet_weights = np.where(
                preferences_adjustet_weights == int(weight),
                int(adjusted_weight),
                preferences_adjustet_weights)
        return preferences_adjustet_weights

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

    def get_min_time(self):
        min_lessons = np.zeros(0)
        for teacher in self._data_container.teachers:
            min_lessons = np.append(min_lessons, teacher.min_lessons)
        return min_lessons

    def get_unadjusted_preferences(self):
        preferences = self._data_container.updated_pref.reshape(-1)
        return preferences


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/testProblem.json"))
    lpData = LPData(container)
    lpData.get_preferences()
