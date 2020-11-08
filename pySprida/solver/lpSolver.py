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
        lessons_bound_start_idx = numTeacher * numGroups * numSubjects
        num_lessons_bounds = int((numTeacher * (numTeacher - 1)) / 2)
        y.extend([m.add_var(var_type=mip.CONTINUOUS) for i in range(num_lessons_bounds)])

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

        idx = 0
        for i in range(numTeacher):
            for j in range(i):
                if i != j:
                    m += (mip.xsum([y[i * numGroups * numSubjects + k] * lessons[k]
                                    for k in range(numGroups * numSubjects)])
                          -
                          mip.xsum([y[j * numGroups * numSubjects + k] * lessons[k]
                                    for k in range(numGroups * numSubjects)])) <= y[lessons_bound_start_idx + idx]
                    m += -(mip.xsum([y[i * numGroups * numSubjects + k] * lessons[k]
                                     for k in range(numGroups * numSubjects)])
                           -
                           mip.xsum([y[j * numGroups * numSubjects + k] * lessons[k]
                                     for k in range(numGroups * numSubjects)])) <= y[lessons_bound_start_idx + idx]
                    idx += 1

        # max one teacher
        co_ref = self.data_container.get_teacher_co_ref()
        ref = [int(not tmp) for tmp in co_ref]
        praev_idx = self.data_container.get_subject_names()
        praev_idx = praev_idx.index("Praevention")
        num_groups = self.data_container.num_groups
        praevention_ids = [i for i in range(praev_idx*num_groups, (praev_idx + 1)*numGroups)]
        for i in range(numGroups * numSubjects):
            if lessonExisting[i] and i not in praevention_ids:
                m += mip.xsum([y[j * numGroups * numSubjects + i] * ref[j] for j in range(numTeacher)]) == 1

        for i in range(numGroups * numSubjects):
            if lessonExisting[i] and i not in praevention_ids:
                m += mip.xsum([y[j * numGroups * numSubjects + i] for j in range(numTeacher)]) <= 2

        #Prävention stuff
        ref_woman_old = self.data_container.get_teacher_woman()
        ref_woman = [int(tmp) for tmp in ref_woman_old]
        ref_man = [int(not tmp) for tmp in ref_woman_old]

        for i in range(numGroups * numSubjects):
            if lessonExisting[i] and i in praevention_ids:
                m += mip.xsum([y[j * numGroups * numSubjects + i] * ref_woman[j] for j in range(numTeacher)]) >= 1
                m += mip.xsum([y[j * numGroups * numSubjects + i] * ref_man[j] for j in range(numTeacher)]) >= 1
                m += mip.xsum([y[j * numGroups * numSubjects + i] for j in range(numTeacher)]) <= 2

        # constraint prios
        # set target
        preferences = self.problem.get_preferences()
        lesson_diff_weights = np.zeros((num_lessons_bounds))
        lesson_diff_weights[:] = -0.1
        weights = np.concatenate((preferences, lesson_diff_weights))
        target = mip.xsum(y[i] * weights[i] for i in range(numTeacher * numGroups * numSubjects + num_lessons_bounds))
        m.objective = mip.maximize(target)

        status = m.optimize(max_seconds=20)
        if status == mip.OptimizationStatus.OPTIMAL:
            print('optimal solution cost {} found'.format(m.objective_value))
        elif status == mip.OptimizationStatus.FEASIBLE:
            print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
        elif status == mip.OptimizationStatus.NO_SOLUTION_FOUND:
            print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
        if status == mip.OptimizationStatus.OPTIMAL or status == mip.OptimizationStatus.FEASIBLE:
            print(f"solution: {status}")

        sol = np.array([v.x for v in m.vars[:lessons_bound_start_idx]])
        return Solution(sol, self.data_container, self.problem)
