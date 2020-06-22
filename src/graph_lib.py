import sys
import pandas as pd
from graph_tool.all import *


import process_matrix as mat

def print_mst(mst, matrix):
    default_font_size = 9
    vertex_names = mat.get_vertex_names(mst, matrix)
    vertex_names_size = mst.new_vertex_property("int", vals=default_font_size)
    # Wypisywanie drzewa:
    u = GraphView(mst)
    graph_draw(u, vertex_text=vertex_names, vertex_font_size=vertex_names_size,
               edge_color=mst.edge_properties["weights"],
               edge_pen_width=mst.edge_properties["weights"])


def make_mst(graph):
    # Zwraca mst grafu graph
    ans = Graph(g=graph)
    ans.set_edge_filter(ans.edge_properties["tree"])
    ans.purge_edges()
    del ans.edge_properties["tree"]
    return ans


def make_graph(matrix):
    g = Graph(directed = False)
    eprops = [g.new_ep("float")]
    edges = mat.get_edge_list(matrix)
    # zwraca mape dla wierzchokow
    Vprop = g.add_edge_list(edges, hashed=True, eprops=eprops)

    g.edge_properties["weights"] = mat.get_weights_edge_property_map(matrix, g);
    g.edge_properties["tree"] = min_spanning_tree(g, weights=g.edge_properties["weights"])
    return g


def test_func(path: str, start: str, end: str):
    correlations = mat.extract_companies_correlations(path, start, end)
    g = make_graph(correlations)
    mst = make_mst(g)
    print_mst(mst, correlations)
    mat.show_vertex_degree(g, g.edge_properties["tree"])



def main(path):
    test_func(path, '20200000', '30000000')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Stooq/sheets")

    sys.exit(main(args[0]))
