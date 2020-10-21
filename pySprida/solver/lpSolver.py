import mip

from pySprida.data.lpData import LPData
from pySprida.data.solution import Solution
from pySprida.solver.solver import Solver

import numpy as np


class LPSolver(Solver):

    def __init__(self, problem, data_container):
        super().__init__(problem, data_container)
        if not isinstance(problem, LPData):
            raise AttributeError("LPSolver does only support LPData as a problem")

    def solve(self) -> Solution:
        m = mip.Model(sense=mip.MAXIMIZE, solver_name=mip.CBC)

        # create variables
        n = 10
        numBetreuer = 5  # anzahl der betreuer
        lenBetreuer = 5  # length of vector per betreuer

        y = [m.add_var(var_type=mip.BINARY) for i in range(n)]

        # add constraints
        # m += x + y <= 10

        # constraint gesamtdauer
        for i in range(numBetreuer):
            m += mip.xsum(
                gesamtdauer[i % lenBetreuer] * y[i] for j in range(0, numBetreuer) for i in range(j, j + lenBetreuer))

        # constraint prios

        # set target
        m.objective = mip.minimize(mip.xsum(c[i] * x[i] for i in range(n)))

        return Solution(np.random.randint(0, 2, (15 * 11 * 3)), self.data_container)
