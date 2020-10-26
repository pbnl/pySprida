import mip

from pySprida.data.lpData import LPData
from pySprida.data.solution import Solution
from pySprida.solver.solver import Solver

import numpy as np


class LPSolver(Solver):

    def __init__(self, problem, data_container):
        super().__init__(problem, data_container)
        self.problem: LPData = problem
        if not isinstance(problem, LPData):
            raise AttributeError("LPSolver does only support LPData as a problem")

    def solve(self) -> Solution:
        m = mip.Model(sense=mip.MAXIMIZE, solver_name=mip.CBC)

        # create variables
        numTeacher = self.problem.get_num_teche()
        numGroups = self.problem.get_num_groups()
        numSubjects = self.problem.get_num_subjects()

        y = [m.add_var(var_type=mip.BINARY) for i in range(numTeacher * numGroups * numSubjects)]

        # constraint group has subject
        lessonExisting = self.problem.lesson_exist_list()
        for i in range(numTeacher * numGroups * numSubjects):
            lessonNumber = i % (numGroups * numSubjects)
            val = lessonExisting[lessonNumber]
            if not val:
                m += y[i] == 0

        # max lessons
        max_lessons = self.problem.get_max_time()
        lessons = self.problem.get_lessons_per_subject()
        for i in range(numTeacher):
            m += mip.xsum([y[i * numGroups * numSubjects + j] * lessons[j]
                           for j in range(numGroups * numSubjects)]) <= max_lessons[i]

        # max one teacher
        for i in range(numGroups * numSubjects):
            if lessonExisting[i]:
                m += mip.xsum([y[j * numGroups * numSubjects + i] for j in range(numTeacher)]) == 1

        # constraint gesamtdauer
        # for i in range(numBetreuer):
        #    m += mip.xsum(
        #        gesamtdauer[i % lenBetreuer] * y[i] for j in range(0, numBetreuer) for i in range(j, j + lenBetreuer))

        # constraint prios

        # set target
        preferences = self.problem.get_preferences()
        pref_target = mip.xsum(y[i] * preferences[i] for i in range(numTeacher * numGroups * numSubjects))
        target = pref_target
        m.objective = mip.maximize(target)

        status = m.optimize(max_seconds=20)
        if status == mip.OptimizationStatus.OPTIMAL:
            print('optimal solution cost {} found'.format(m.objective_value))
        elif status == mip.OptimizationStatus.FEASIBLE:
            print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
        elif status == mip.OptimizationStatus.NO_SOLUTION_FOUND:
            print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
        if status == mip.OptimizationStatus.OPTIMAL or status == mip.OptimizationStatus.FEASIBLE:
            print('solution:')

        sol = np.array([v.x for v in m.vars])
        return Solution(sol, self.data_container)
