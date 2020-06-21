import sys
import pandas as pd
from graph_tool.all import *


import process_matrix as mat
from general_parser_functions import get_matrix

def print_mst(graph, matrix, tree_map):
    # PropertyMap z nazwami spółek
    # todo np. wypisywanie nazw tylko wierzcholkow o danych stopniach
    default_font_size = 9
    vertex_names = mat.get_vertex_names(graph, matrix)
    vertex_names_size = graph.new_vertex_property("int", vals=default_font_size)
    # Wypisywanie drzewa:
    u = GraphView(graph, efilt=tree_map)
    graph_draw(u, vertex_text=vertex_names, vertex_font_size=vertex_names_size)


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
    tree_map = min_spanning_tree(g, weights=weights)
    print_mst(g, matrix, tree_map)
    return g


def main(path):
    g = make_graph(mat.calc_correlations(get_matrix(path)))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Stooq/sheets")

    sys.exit(main(args[0]))
