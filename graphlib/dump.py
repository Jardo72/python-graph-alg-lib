from graphlib.algorithms import ShortestPathSearchResult
from graphlib.graph import AbstractGraph

def dump_graph(graph: AbstractGraph):
    """Dumps the vertices and edges of the given graph to stdout.

    The dump is generated in a structured way, and it also includes the weights
    of the edges.

    Args:
        graph (AbstractGraph): The graph to be dumped.
    """
    weighted = 'YES' if graph.is_weighted else 'NO'
    print()
    print(f'Graph type: {graph.graph_type}')
    print(f'Weighted: {weighted}')
    print(f'Vertices (totally {graph.vertex_count}):')
    for current_vertex in graph.get_sorted_vertices():
        print(f' - {current_vertex}')
    print('Edges:')
    for current_vertex in graph.get_sorted_vertices():
        for adjacent_vertex in graph.get_adjacent_vertices(current_vertex):
            weight = graph.get_edge_weight(current_vertex, adjacent_vertex)
            print(f' - {current_vertex} -> {adjacent_vertex} (weight = {weight})')


def dump_shortest_path(shortest_path: ShortestPathSearchResult):
    """Dumps the given shortest path to stdout.

    Args:
        shortest_path (ShortestPathSearchResult): The shortest path to be dumped.
    """
    print()
    print(f'Shortest path from {shortest_path.start} to {shortest_path.destination}')
    print(f'Overall distance {shortest_path.overall_distance}')
    print('Path:')
    for edge in shortest_path.path:
        print(f' - {edge.start} -> {edge.destination} (weight = {edge.weight})')
