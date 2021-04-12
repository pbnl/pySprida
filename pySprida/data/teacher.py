from typing import List
import numpy as np

from pySprida.data.groupType import GroupType


class Teacher:
    def __init__(self, container, name, short_name, preferences, max_lessons, woman, co_ref, min_lessons):
        self.min_lessons: int = min_lessons
        self.name: str = name
        self.short_name: str = short_name
        self.preferences: List[int] = preferences
        self.max_lessons: int = max_lessons
        self.container = container
        self.woman = woman
        self.co_ref = co_ref

    def get_subject_preferences(self, min_preference=1):
        subjects = []
        for i, pref_arrray in enumerate(self.preferences):
            for j, pref in enumerate(pref_arrray):
                if pref >= min_preference:
                    subject = self.container.group_types[j].existing_noneexisting_subjects[i]
                    if subject is not None:
                        subjects.append(subject)
                    else:
                        raise ValueError(
                            f"{self.name} has a preference > 0 for class {i}_{j}. But this subject does not exist in this class configuration!")
        return subjects

    def get_all_subject_preferences(self):
        prefs = []
        for group in self.container.groups:
            gtype: GroupType = group.group_type
            gid = gtype.id
            group_prefs = []
            for i, sub in enumerate(gtype.existing_noneexisting_subjects):
                pref = self.preferences[i][gid]
                group_prefs.append(pref)
            prefs.append(group_prefs)
        return np.transpose(np.array(prefs))