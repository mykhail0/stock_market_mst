"""
    Moduł oferuje funkcje przetwarzające DataFrame wektorów spółek.
    Jest pewnym mostem pomiędzy raw "tablicową" reprezentacją danych spółek
    a grafową reprezentacją.
"""
import os
import sys
import numpy as np
import pandas as pd
from graph_tool.all import *
from graph_tool import new_edge_property
from math import sqrt, isnan

from general_parser_functions import get_matrix


def calc_vectors(matrix):
    # Liczy wektor spółki na podstawie danych.
    # (wg trzeciej metody w pracy magisterskiej Sienkiewicza)
    tmp = pd.DataFrame(matrix)
    return matrix.diff().div(tmp)

def calc_correlations(matrix):
    # Liczy współczynniki korelacji dla danego DataFrame.
    # Np. matrix to wektory spółek
    return matrix.corr()


def get_edge_list(matrix):
# tworzy listę krawędzi
    ans = np.empty(shape = (matrix.shape[0] * (matrix.shape[0] - 1) // 2, 3),
                   dtype = object)
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

def calculate_vertices_distance(correlation):
    # Liczy odległość między spółkami w metryce ze źródeł
    # zakłada, że wsp. korelacji są mniejsze od 1, 
    # w innym wypadku przyjmuje ich wartość jako 1.
    # Jeśli trafił się NaN, przyjmujemy że to współczynnik o wartości 0.
    if isnan(correlation):
        return calculate_vertices_distance(0)
    elif correlation > 1:
        return calculate_vertices_distance(1)
    else:
        return sqrt(2 * (1 - correlation))

def get_weights_edge_property_map(matrix, graph):
# tworzy obiekt edge_property_map z wagami krawędzi
# na podstawie tablicy współczynników korelacji
# UWAGA - wersja beta, zaklada że wierzchołki są numerowane po kolei,
# 0 to pierwsza firma w rzędzie/kolumnie, 1 druga itd.
    weights_map = graph.new_edge_property("short")
    # totalna januszerka, ale nie umiem zmienić wierchołka w liczbę
    source_index = 0
    target_index = 1
    for edge in graph.edges():
        correlation = matrix.iat[source_index, target_index]
        weights_map[edge] = calculate_vertices_distance(correlation)
        target_index += 1
        if(target_index == graph.num_vertices()):
            source_index += 1
            target_index = source_index + 1
    return weights_map


def main(path: str):
    print(calc_vectors(get_matrix(path)))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/directory/with/sheets.cvs")

    sys.exit(main(args[0]))
