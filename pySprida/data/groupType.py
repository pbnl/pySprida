from typing import List

from pySprida.data.subject import Subject


class GroupType:
    def __init__(self, container, name, existing_noneexisting_subjects, id):
        self.container = container
        self.name: str = name
        self.existing_noneexisting_subjects: List[Subject] = existing_noneexisting_subjects
        self.id = id

    def link_subjects(self):
        for sub in self.teached_subjects:
            sub.group_type = self

    @property
    def teached_subjects(self):
        teached_subjects = []
        for subject in self.existing_noneexisting_subjects:
            if subject is not None:
                teached_subjects.append(subject)
        return teached_subjects