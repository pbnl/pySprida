from pySprida.data.solution import Solution


class Solver():

    def __init__(self, problem, data_container):
        self.problem = problem
        self.data_container = data_container

    def solve(self) -> Solution:
        pass