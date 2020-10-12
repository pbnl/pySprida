from pySprida.data.subjectType import SubjectType


class Subject:

    def __init__(self, container, subject_type, num_lessons):
        self.container = container
        self.subject_type: SubjectType = subject_type
        self.num_lessons: int = num_lessons
        self.group_type = None

    @property
    def name(self):
        return f"{self.subject_type.name}_{self.group_type.name}"