from pySprida.data.dataContainer import DataContainer
import numpy as np


class Solution:

    def __init__(self, solution_data, data_container: DataContainer, problem):
        self.solution_data = solution_data
        self._data_container = data_container
        self.problem = problem

    def get_mapping_matrix(self):
        num_teacher = self._data_container.num_teacher
        matrix = self.solution_data.reshape(
            (num_teacher,
             self.solution_data.shape[0] // num_teacher
             )
        )
        return matrix

    def get_teacher_num_lessons(self):
        num_lessons = []
        numTeacher = self.problem.get_num_teche()
        numGroups = self.problem.get_num_groups()
        numSubjects = self.problem.get_num_subjects()
        lessons = self.problem.get_lessons_per_subject()
        for i in range(numTeacher):
            num_lessons.append(sum([self.solution_data[i * numGroups * numSubjects + j] * lessons[j]
                                    for j in range(numGroups * numSubjects)]))
        return np.array(num_lessons)
