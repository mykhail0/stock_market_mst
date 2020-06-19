import sys
import pandas as pd
from graph_tool.all import *


import process_matrix as mat
from general_parser_functions import get_matrix


def make_graph(matrix):
    g = Graph(directed = False)
    eprops = [g.new_ep("float")]
    edges = mat.get_edge_list(matrix)
    # idk why ale gdy wyrzuciem string_vals = True, to zaczelo dzialac, stara wersja:
    # g.add_edge_list(edges, hashed = True, string_vals = True, eprops = eprops)
    # zwraca mape dla wierzchokow
    Vprop = g.add_edge_list(edges, hashed=True, eprops=eprops)
    weights = mat.get_weights_edge_property_map(matrix, g)
    # Usunąłem vertex z argumentów, teraz tworzy za pomocą algorytmu Kruskala.
    tree_map = min_spanning_tree(g, weights = weights)
    # Wypisywanie drzewa:
    u = GraphView(g, efilt=tree_map)
    graph_draw(u)
    return g


def main(path):
    g = make_graph(mat.calc_correlations(mat.calc_vectors(get_matrix(path))))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Stooq/sheets")

    sys.exit(main(args[0]))
