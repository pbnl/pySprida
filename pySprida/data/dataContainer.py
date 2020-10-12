import json
from pathlib import Path
import logging
from typing import List
import numpy as np
from pySprida.data.group import Group
from pySprida.data.groupType import GroupType
from pySprida.data.subject import Subject
from pySprida.data.subjectType import SubjectType
from pySprida.data.teacher import Teacher


class DataContainer:

    def __init__(self):
        self._data = None
        self.subject_types: List[SubjectType] = []
        self.group_types: List[GroupType] = []
        self.groups: List[Group] = []
        self.teachers: List[Teacher] = []

    @property
    def subjects(self):
        subjects = []
        for grou_type in self.group_types:
            for sub in grou_type.existing_noneexisting_subjects:
                subjects.append(sub)
        return subjects

    def load_data(self, path: Path):
        logging.debug("Loading json data")
        with open(path) as f:
            d = json.load(f)
            self._data = d

        self.load_subject_types(self._data["config"])
        self.load_group_types(self._data["config"])
        self.load_groups(self._data["config"])
        self.load_teachers(self._data["teachers"])
        logging.debug("Loaded json data")

    def load_subject_types(self, config):
        subs = config["subjects"]
        for sub in subs:
            self.subject_types.append(SubjectType(
                container=self,
                name=sub["name"]
            ))

    def load_group_types(self, config):
        group_types = config["groupTypes"]
        subjects = config["subjects"]
        for i, group_type in enumerate(group_types):
            existing_noneexisting_subjects = []
            for j, subject in enumerate(subjects):
                num = subject["lessons_in_group_types"][i]
                if num > 0:
                    existing_noneexisting_subjects.append(Subject(
                        container=self,
                        subject_type=self.subject_types[j],
                        num_lessons=num))
                else:
                    existing_noneexisting_subjects.append(None)
            self.group_types.append(GroupType(
                container=self,
                name=group_type,
                existing_noneexisting_subjects=existing_noneexisting_subjects
            ))
            for group_type in self.group_types:
                group_type.link_subjects()

    def load_groups(self, config):
        num_groups = config["numGroups"]
        for grouptype_id, num in enumerate(num_groups):
            for i in range(num):
                self.groups.append(Group(
                    container=self,
                    group_type=self.group_types[grouptype_id],
                    name=f"{self.group_types[grouptype_id].name}_{i}"))

    def load_teachers(self, teachers):
        for teacher in teachers:
            self.teachers.append(Teacher(
                container=self,
                name=teacher["name"],
                short_name=teacher["shortName"],
                preferences=teacher["preferences"],
                max_lessons=teacher["maxLessons"]
            ))

    @property
    def num_teacher(self):
        return len(self.teachers)

    @property
    def num_cources(self):
        return len(self.subject_types) * len(self.groups)

    @property
    def num_groups(self):
        return len(self.groups)

    def get_preference_matrix(self):
        preferences = np.zeros((self.num_teacher, self.num_cources))
        for i, teacher in enumerate(self.teachers):
            preferences[i] = np.array(teacher.preferences).reshape(-1)
        return preferences

    def get_teacher_names(self):
        return [teacher.name for teacher in self.teachers]

    def get_group_names(self):
        return [group.name for group in self.groups]

    def get_subject_names(self):
        return [subject.name for subject in self.subject_types]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/testProblem.json"))
    printer.printTeachers(container)
    printer.printGroups(container)