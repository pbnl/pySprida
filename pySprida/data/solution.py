import mip

from pySprida.data.dataContainer import DataContainer
import numpy as np


class Solution:

    def __init__(self, solution_data,
                 data_container: DataContainer,
                 problem,
                 log,
                 loss,
                 status,
                 relaxed_loss):
        self.solution_data = solution_data
        self._data_container = data_container
        self.problem = problem
        self.log = log
        self.loss = loss
        self.status = status
        self.relaxed_loss = relaxed_loss

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

    @property
    def status_name(self):
        if self.status == mip.OptimizationStatus.OPTIMAL:
            return "Optimal: Best solution found"
        elif self.status == mip.OptimizationStatus.FEASIBLE:
            return "Feasible: Good solution found. But I maybe find better one with mor time."
        elif self.status == mip.OptimizationStatus.INFEASIBLE:
            return "There is no solution"
        elif self.status == mip.OptimizationStatus.INT_INFEASIBLE:
            return "There is just a solution for the relaxed problem"
        elif self.status == mip.OptimizationStatus.NO_SOLUTION_FOUND:
            return "No integer feasible solution was found: Maybe I need more time"
        else:
            return "Error"