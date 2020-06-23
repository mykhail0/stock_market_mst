"""
    Moduł oferuje funkcje przetwarzające DataFrame wektorów spółek.
    Jest pewnym mostem pomiędzy raw "tablicową" reprezentacją danych spółek
    a grafową reprezentacją.
"""
import os
import sys
import numpy as np
import pandas as pd
#needed for plots
import matplotlib.pyplot as pyplot

from graph_tool.all import *
from graph_tool import new_edge_property
from math import sqrt, isnan

from general_parser_functions import get_matrix

def show_vertex_degree(graph):
    max = 0
    for v in graph.vertices():
        k = v.out_degree()
        if k > max:
            max = k

    sum = []
    i = 0
    while i < max + 1:
        sum.append(0)
        i += 1
    for v in graph.vertices():
        sum[v.out_degree()] += 1

    df = pd.DataFrame(data=sum, columns=['vertex count'])
    df = df.loc[~(df==0).all(axis=1)]
    df['degree'] = df.index
    df.plot(x='degree', y='vertex count', kind='scatter')
    pyplot.yscale('log')
    pyplot.xscale('log')
    pyplot.show()



def cut_time_dataframe(df, start: str, end: str):
    # Ucina daty w formacie RRRRMMDD
    return df.loc[start : end]


def rm_companies_w_little_data(matrix, percent: float):
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


def calc_vectors(matrix):
    # Liczy wektor spółki na podstawie danych.
    # (wg trzeciej metody w pracy magisterskiej Sienkiewicza)
    tmp = pd.DataFrame(matrix)
    return matrix.diff().div(tmp)


# TL;DR daje macierz ze wsp. korelacji spółek.
def extract_companies_correlations(path: str, start = '20200000', end = '30000000', percent = 0):
    # Z arkuszy w ścieżce `path` wyciąga DataFrame z
    # interesującymi nas notowaniami w kolejnych dniach dla wszystkich firm.
    # Następnie ucina DF do interesującego nas przedziału,
    # a potem odrzuca z DF firmy, które mają procent NaN-ów, przekraczający
    # `percent`. Dalej wylicza wektory spółek, po czym korelacje spółek.
    return calc_vectors(rm_companies_w_little_data(cut_time_dataframe(get_matrix(path), start, end), percent)).corr()


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
        # *10 żeby linie w wyświetlanym grafie były odpowiedniej grubości
        return 10 * sqrt(2 * (1 - correlation))


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
    print(extract_companies_correlations(path))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/directory/with/sheets.cvs")

    sys.exit(main(args[0]))
