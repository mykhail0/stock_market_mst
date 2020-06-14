import sys
import pandas as pd
from graph_tool.all import *
from process_matrix import get_edge_list, get_edge_property_map
from parse_txt import get_correlation_matrix


def make_graph(matrix):
    g = Graph(directed = False)
    eprops = [g.new_ep("float")]
    edges = get_edge_list(matrix)
#nwm czemu ale tu odmawia dzialania
    #idk why ale gdy wyrzuciem string_vals = True, to zaczelo dzialac, stara wersja:
    #g.add_edge_list(edges, hashed = True, string_vals = True, eprops = eprops)
    g.add_edge_list(edges, hashed=True,eprops=eprops)
    #todo - zrobić funkcję odpowiadającą za wagi
    weights = get_edge_property_map(matrix)
    tree_map = min_spanning_tree(g, weights = weights, vertex = g.vertex(0))
    return g


def main(path):
    g = make_graph(get_correlation_matrix(path))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Stooq/sheets")

    sys.exit(main(args[0]))
