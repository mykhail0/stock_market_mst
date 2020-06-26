import sys
import pandas as pd
from graph_tool.all import *

import process_matrix as mat


def print_mst(g):
    default_font_size = 9
    vertex_names_size = g.new_vertex_property("int", vals=default_font_size)
    # Wypisywanie drzewa:
    u = GraphView(g)
    graph_draw(u, vertex_text=g.vertex_properties["names"],
               vertex_font_size=vertex_names_size,
               edge_color=g.edge_properties["weights"],
               edge_pen_width=g.edge_properties["weights"])


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

    g.edge_properties["weights"] = mat.get_weights_edge_property_map(matrix, g)
    g.edge_properties["tree"] = min_spanning_tree(g, weights=g.edge_properties["weights"])
    g.vertex_properties["names"] = mat.get_vertex_names(g, matrix)
    return g

def compute_MHSD(g):
    dist_map = shortest_distance(g)
    sum=0
    count=0
    for v in g.vertices():
        for i in dist_map[v]:
            sum+=i
            count+=1
        #bo jedna odległość to 0 i się nie liczy
        count-=1

    # dwa razy policzyliśmy tę samą odległość
    sum = sum // 2

    return sum / count


def mol(g, v):
    dist = shortest_distance(g, source = v)
    return dist.a.sum() / g.num_vertices()

def top_n_molwise(g, n):
    top=[]
    l=0
    while l<n:
        min_vertex_value=9999999999999999999999999999
        min_vertex= None
        for v in g.vertices():
            ok=0
            for i in top:
                if i==v:
                    ok=1
            k=mol(g, v)
            if ok==0 and min_vertex_value > k:
                min_vertex=v
                min_vertex_value=k
        top.append(min_vertex)
        l+=1
    return top


def print_top_mol(top, g):
    for i in top:
        print(g.vp.names[i]+": "+str(mol(g, i)))

def top_n_degreewise(graph,n):
    top=[]
    l=0
    while l<n:
        max_vertex_value=0
        max_vertex= None
        for v in graph.vertices():
            ok=0
            for i in top:
                if i==v:
                    ok=1
            k=v.out_degree()
            if ok==0 and max_vertex_value < k:
                max_vertex=v
                max_vertex_value=k
        top.append(max_vertex)
        l+=1
    return top

def print_top_degree(top, vertex_names):
    for i in top:
        print(vertex_names[i]+": "+str(i.out_degree()))


def get_vertex(g, name: str):
    for v in g.vertices():
        if g.vp.names[v] == name:
            return v
    return None

def test_func(path: str, start: str, end: str):
    correlations = mat.extract_companies_correlations(path, start, end)
    g = make_graph(correlations)
    mst = make_mst(g)



def main(path):
    test_func(path, '20200000', '30000000')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Stooq/sheets")

    sys.exit(main(args[0]))
