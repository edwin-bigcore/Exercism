class Matrix:

    def __init__(self, matrix_string):
        self.matrix = [row.split() for row in matrix_string.splitlines()]

    def row(self, index):
        return [int(col) for col in self.matrix[index-1]]

    def column(self, index):
        return [int(row[index-1]) for row in self.matrix]

def matrix_1(matrix_string,index):
    matrix = [row.split() for row in matrix_string.splitlines()]
    return [int(matrix[i][index-1]) for i in range(len(matrix))]
    
def matrix_2(matrix_string,index):
    matrix = [row.split() for row in matrix_string.splitlines()]
    return [int(row[index-1]) for row in matrix]
    

if __name__=='__main__':
    import timeit
    
    #print(matrix_1('1 2 3\n4 5 6\n7 8 9\n8 7 6', 3))
    #print(matrix_2('1 2 3\n4 5 6\n7 8 9\n8 7 6', 3))
    
    print(timeit.repeat(r"matrix_1('1 2 3\n4 5 6\n7 8 9\n8 7 6', 3)", setup='from __main__ import matrix_1', repeat=3, number=100000))
    print(timeit.repeat(r"matrix_2('1 2 3\n4 5 6\n7 8 9\n8 7 6', 3)", setup='from __main__ import matrix_2', repeat=3, number=100000))