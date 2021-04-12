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
        self.solver_config = None
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
        self.load_solvers(self._data["config"])
        logging.debug("Loaded json data")

        if "updated_preferences" in self._data:
            self.updated_pref = np.array(self._data["updated_preferences"])
        else:
            self.updated_pref = self.get_preference_matrix()

    def load_subject_types(self, config):
        subs = config["subjects"]
        for i, sub in enumerate(subs):
            self.subject_types.append(SubjectType(
                container=self,
                name=sub["name"],
                id=i
            ))

    def load_group_types(self, config):
        group_types = config["groupTypes"]
        subjects = config["subjects"]
        for group_type_id, group_type in enumerate(group_types):
            existing_noneexisting_subjects = []
            for j, subject in enumerate(subjects):
                num = subject["lessons_in_group_types"][group_type_id]
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
                existing_noneexisting_subjects=existing_noneexisting_subjects,
                id=group_type_id
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
                max_lessons=teacher["maxLessons"],
                co_ref=bool(teacher["coRef"]),
                woman=bool(teacher["woman"]),
                min_lessons=teacher.get("min_lessons", 0)
            ))

    @property
    def num_teacher(self):
        return len(self.teachers)

    @property
    def num_cources(self):
        return len(self.subject_types) * len(self.groups)

    @property
    def num_subjects(self):
        return len(self.subject_types)

    @property
    def num_groups(self):
        return len(self.groups)

    def get_preference_matrix(self):
        preferences = np.zeros((self.num_teacher, self.num_cources))
        for i, teacher in enumerate(self.teachers):
            preferences[i] = np.array(teacher.get_all_subject_preferences()).reshape(-1)
        return preferences

    def get_teacher_names(self):
        return [teacher.name for teacher in self.teachers]

    def get_group_names(self):
        return [group.name for group in self.groups]

    def get_subject_names(self):
        return [subject.name for subject in self.subject_types]

    def get_teacher_co_ref(self):
        return [teacher.co_ref for teacher in self.teachers]

    def get_teacher_woman(self):
        return [teacher.woman for teacher in self.teachers]

    def load_solvers(self, param):
        self.solver_config = param["solver"]
        # TODO: Support other solvers

    def to_json(self):
        data = {"config": {}}
        data["config"]["groupTypes"] = [gtype.name for gtype in self.group_types]
        num_groups = []
        for gtype in self.group_types:
            num = 0
            for group in self.groups:
                if group.group_type == gtype:
                    num += 1
            num_groups.append(num)
        data["config"]["numGroups"] = num_groups
        data["config"]["solver"] = self.solver_config
        subjects = []
        for sub in self.subject_types:
            lessons_in_group = []
            for gtype in self.group_types:
                found = False
                for sub_in_gtype in gtype.existing_noneexisting_subjects:
                    if sub_in_gtype is not None:
                        if sub == sub_in_gtype.subject_type:
                            lessons_in_group.append(sub_in_gtype.num_lessons)
                            found = True
                            break
                if not found:
                    lessons_in_group.append(0)

            subject = {
                "name": sub.name,
                "lessons_in_group_types": lessons_in_group
            }
            subjects.append(subject)
        data["config"]["subjects"] = subjects

        teachers = []
        for teacher in self.teachers:
            tdata = {
                "coRef": teacher.co_ref,
                "maxLessons": teacher.max_lessons,
                "name": teacher.name,
                "shortName": teacher.short_name,
                "woman": teacher.woman,
                "preferences": teacher.preferences
            }
            teachers.append(tdata)
        data["teachers"] = teachers
        data["updated_preferences"] = self.updated_pref.tolist()
        return data


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pySprida.data.consolePrinter import ConsolePrinter
    printer = ConsolePrinter()

    container = DataContainer()
    container.load_data(Path("./testData/testProblem.json"))
    printer.printTeachers(container)
    printer.printGroups(container)
