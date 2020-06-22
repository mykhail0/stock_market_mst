import sys
import pandas as pd
from graph_tool.all import *


import process_matrix as mat


def print_mst(graph, matrix, tree_map, weights):
    # PropertyMap z nazwami spółek
    # todo np. wypisywanie nazw tylko wierzcholkow o danych stopniach
    default_font_size = 9
    vertex_names = mat.get_vertex_names(graph, matrix)
    vertex_names_size = graph.new_vertex_property("int", vals=default_font_size)
    # Wypisywanie drzewa:
    u = GraphView(graph, efilt=tree_map)
    graph_draw(u, vertex_text=vertex_names, vertex_font_size=vertex_names_size,
               edge_color=weights, edge_pen_width=weights)


def make_graph(matrix):
    g = Graph(directed = False)
    eprops = [g.new_ep("float")]
    edges = mat.get_edge_list(matrix)
    # zwraca mape dla wierzchokow
    Vprop = g.add_edge_list(edges, hashed=True, eprops=eprops)
    return g


def test_func(path: str, start: str, end: str):
    correlations = mat.extract_companies_correlations(path, start, end)
    g = make_graph(correlations)
    weights = mat.get_weights_edge_property_map(correlations, g)
    tree_map = min_spanning_tree(g, weights=weights)
    print_mst(g, correlations, tree_map, weights)
    mat.show_vertex_degree(g, tree_map)



def main(path):
    test_func(path, '20200000', '30000000')



if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Stooq/sheets")

    sys.exit(main(args[0]))
