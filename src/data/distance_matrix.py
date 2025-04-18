import numpy as np
from scipy.sparse.csgraph import floyd_warshall


def calculate_distamnce_matrix(G):
    """
    Computes the all-pairs shortest path distance matrix for a given graph using optimized Floyd-Warshall algorithm.
    Returns: numpy.ndarray (2D array representing the shortest distance between all pairs of nodes in the graph)
    """
    nodes = list(G.nodes)
    n = len(nodes)
    print(f"Number of nodes: {n}")

    node_index = {node: idx for idx, node in enumerate(nodes)}
    print("Creating adjacency matrix")

    # Creating adjacency matrix
    D = np.full((n, n), np.inf)

    for u, v, data in G.edges(data=True):
        length = data.get("length", np.inf)
        i, j = node_index[u], node_index[v]
        D[i, j] = length
        D[j, i] = length

    np.fill_diagonal(D, 0)  # Set diagonal to 0

    # Using optimized Floyd-Warshall
    D = floyd_warshall(D, directed=False)
    return D

def distance_matrix(G, city_params):
    """
    Returns the precomputed distance matrix if available, otherwise calculates it.
    Returns: numpy.ndarray (2D array representing the shortest distance between all pairs of nodes in the graph)
    """
    if city_params["distance_matrix"]:
        return np.load(city_params["distance_matrix"])
    return calculate_distamnce_matrix(G)