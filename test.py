import numpy as np


class Matrix():
    def __init__(self, type, number_city, weight_section):
        self.type = type
        self.number_city = number_city
        self.weight_section = weight_section
        self.type_list = ['LOWER_DIAG_ROW', 'UPPER_ROW']
        self.weight_section_matrix = np.zeros((self.number_city, self.number_city))

    def lower_diag_row(self):
        """
        weight_section: [0, 1, 0, 2, 3, 0, 4, 5, 6, 0]
        :return: full matrix of lower diag row bellow
            array([[0., 0., 0., 0.],
                   [1., 0., 0., 0.],
                   [2., 3., 0., 0.],
                   [4., 5., 6., 0.]])
        """
        self.weight_section_matrix[np.tril_indices(self.number_city)] = self.weight_section
        for i in range(len(self.weight_section_matrix)):
            for j in range(0, i):
                self.weight_section_matrix[j][i] = self.weight_section_matrix[i][j]
        return self.weight_section_matrix

    def upper_row(self):
        """
        weight_section: [2,3,4,5,6,7]
        :return:
            array([[0., 2., 3., 4.],
                   [0., 0., 5., 6.],
                   [0., 0., 0., 7.],
                   [0., 0., 0., 0.]])
        """
        m = np.zeros((self.number_city - 1, self.number_city - 1))

        m[np.triu_indices(self.number_city - 1)] = self.weight_section

        for i in range(self.number_city-1):
            for j in range(self.number_city-1):
                self.weight_section_matrix[i][j+1] = int(m[i][j])

        for i in range(len(self.weight_section_matrix)):
            for j in range(i, len(self.weight_section_matrix)):
                self.weight_section_matrix[j][i] = self.weight_section_matrix[i][j]
        return self.weight_section_matrix

    def get_weight_section_matrix(self):
        if self.type == 'LOWER_DIAG_ROW':
            self.weight_section_matrix = self.lower_diag_row()
        if self.type == 'UPPER_ROW':
            self.weight_section_matrix = self.upper_row()

        return self.weight_section_matrix


a = Matrix('LOWER_DIAG_ROW', 4, [0, 1, 0, 2, 3, 0, 4, 5, 6, 0])
a.get_weight_section_matrix()
b = Matrix('UPPER_ROW', 4, [2,3,4,5,6,7])
b.get_weight_section_matrix()