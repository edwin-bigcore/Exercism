class Matrix:

    def __init__(self, matrix_string):

        self.matrix=[]

        for row_str in matrix_string.splitlines():
            row=[]
            for col_str in row_str.split(' '):
                row.append(int(col_str))
            self.matrix.append(row)

    def row(self, index):
        return self.matrix[index-1]

    def column(self, index):
        return [self.matrix[i][index-1] for i in range(len(self.matrix))]