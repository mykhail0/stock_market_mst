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

#ucina daty w formacie RRRRMMDD
def cut_time_dataframe(df,start: str,end: str):
    return df.loc[start : end]

def calc_vectors(matrix):
    # Liczy wektor spółki na podstawie danych.
    # (wg trzeciej metody w pracy magisterskiej Sienkiewicza)
    tmp = pd.DataFrame(matrix)
    #obciecie dataframe do danych od poczatku 2020
    tmp= cut_time_dataframe(tmp,'20200000','30000000')
    #usuwanie spolek z NaN-ami
    tmp=rm_companies_w_little_data(0,tmp)
    return matrix.diff().div(tmp)


def calc_correlations(matrix):
    # Oblicza dla spółek ich wektory i wylicza korelacje
    return calc_vectors(matrix).corr()

def rm_companies_w_little_data(percent: int, matrix):
    # percent to liczba z przedziału [0, 1]
    # Usuwane są kolumny z liczbą komórek NaN przekraczającą
    # podany procent.
    # Trzeba uważać na procent, bo każda spółka ma w weekendy NaN'y
    # BTW totalnie niewydajne i mocno Pythonowe
    rows_number = len(matrix.index)
    columns_to_delete = []

    for f in matrix.columns.values.tolist():
        if matrix[f].isna().sum() / rows_number > percent:
            columns_to_delete.append(f)

    return matrix.drop(columns_to_delete, axis = 1)


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
    weights_map = graph.new_edge_property("float")
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

def get_vertex_names(graph, matrix):
#zakłada, że wierzchołki są tworzone po kolei
    names = graph.new_vertex_property("string")
    vertex_count = 0
    for vertex in graph.vertices():
        names[vertex] = matrix.columns.values[vertex_count]
        vertex_count += 1
    return names

def main(path: str):
    print(rm_companies_w_little_data(0, cut_time_dataframe(get_matrix(path),'20200000','30000000')))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/directory/with/sheets.cvs")

    sys.exit(main(args[0]))
