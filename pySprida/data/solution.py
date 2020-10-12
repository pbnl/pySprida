from pySprida.data.dataContainer import DataContainer


class Solution:

    def __init__(self, solution_data, data_container: DataContainer):
        self.solution_data = solution_data
        self._data_container = data_container

    def get_mapping_matrix(self):
        num_teacher = self._data_container.num_teacher
        matrix = self.solution_data.reshape(
            (num_teacher,
             self.solution_data.shape[0] // num_teacher
             )
        )
        return matrix