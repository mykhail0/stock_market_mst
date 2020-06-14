import numpy as np
import sys
import pandas as pd
from graph_tool.all import *
from parse_txt import get_correlation_matrix


def get_edge_list(matrix):
# tworzy listę krawędzi
    ans = np.empty(shape = (matrix.shape[0] * (matrix.shape[0] - 1) // 2, 3), dtype = object)
    i = 1
    count = 0
    for row in matrix.itertuples():
        for j in range(i, matrix.shape[0]):
            ans[count, 0] = row[0]
            ans[count, 1] = matrix.columns[j]
            ans[count, 2] = row[j + 1]
            count += 1
        i += 1
    return ans

def get_edge_property_map(matrix):
    #


def main(path):
    print(get_edge_list(get_correlation_matrix(path)))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Excel/sheet.xls")

    sys.exit(main(args[0]))
