'''
'''
import csv
import numpy as np

mat_data = []
with open('matrices/blosum62.csv', "r", encoding="utf-8") as fhMat:
    matreader = csv.reader(fhMat, delimiter=",")
    next(matreader)
    for row in matreader:
        mat_data.append(row[1:])

matrix = np.asarray(mat_data)
matrix = abs(matrix.astype(float))

diagonals = np.diagonal(matrix)
diag_sum = sum(diagonals)
off_diag_sum = np.sum(matrix) - diag_sum

print("Average Distance:", off_diag_sum / (matrix.size-diagonals.size))
