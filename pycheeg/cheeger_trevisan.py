"""
An implementation of the Cheeger-Trevisan algorithm for networkx graphs.
"""
import scipy as sp
import scipy.sparse
import scipy.sparse.linalg
import numpy as np
import networkx as nx


def two_sided_sweep(adjacency_matrix, top_eigenvector, degrees):
    """
    Given a (positive and negative) vector on the vertices in the graph G, run the two-sided sweep set algorithm to
    find an almost-bipartite set.

    :param adjacency_matrix: The adjacency matrix of the graph to use.
    :param top_eigenvector: the top eigenvector of the graph laplacian matrix.
    :param degrees: A list with the degree of each vertex in the graph.
    :return: A tuple containing:
      - L - the vertices in the left set
      - R - the vertices in the right set
    """
    # Calculate n here once
    n = adjacency_matrix.shape[0]

    # Keep track of the best cut so far
    best_bipartiteness = None
    best_left_set = None
    best_right_set = None

    # Keep track of the size of the set and the cut weight to make computing the bipartiteness straightforward.
    # The cut weight is the numerator of the bipartiteness:
    #   2 w(L, L) + 2 w(R, R) + w(L union R, V \ L union R)
    total_volume = np.sum(degrees)
    set_volume = 0
    set_size = 0
    bipart_numerator = 0

    # Normalise the eigenvector with the degrees of each vertex
    degree_matrix = sp.sparse.diags(degrees, 0)
    top_eigenvector = degree_matrix.power(-(1/2)).dot(top_eigenvector)

    # First, sort the vertices based on their absolute value in the second eigenvector
    sorted_vertices = [i for i, v in sorted(enumerate(top_eigenvector), key=(lambda y: -abs(y[1])))]

    # Keep track of which edges to add/subtract from the cut each time
    # These vectors indicate whether to add or subtract the weight of edges to each vertex when adding a new vertex
    # to the left of the right set.
    left_update_vector = np.ones(n)
    right_update_vector = np.ones(n)

    # Loop through the vertices in the graph, adding them to the left or right set depending on their value in the
    # given eigenvector.
    current_left_set = []
    current_right_set = []
    for (i, v) in enumerate(sorted_vertices[:-1]):
        # Update the set size and volume
        set_volume += degrees[v]
        set_size += 1

        if top_eigenvector[v] < 0:
            # We will add this node to the left set
            current_left_set.append(v)

            # From now on, edges to this vertex from vertices in the right set will be removed from the cut
            right_update_vector[v] = -1

            # Compute the additional weight incurred by adding this vertex to the left set
            additional_weight = adjacency_matrix[v, :].dot(left_update_vector)
        else:
            # We will add this node to the right set
            current_right_set.append(v)

            # From now on, edges to this vertex from vertices in the left set will be removed from the cut
            left_update_vector[v] = -1

            # Compute the additional weight incurred by adding this vertex to the right set
            additional_weight = adjacency_matrix[v, :].dot(right_update_vector)

        # Calculate the bipartiteness
        bipart_numerator += additional_weight
        this_bipartiteness = bipart_numerator / min(set_volume, total_volume - set_volume)

        # Check whether this bipartiteness is the best
        if best_bipartiteness is None or this_bipartiteness < best_bipartiteness:
            best_bipartiteness = this_bipartiteness
            best_left_set = current_left_set.copy()
            best_right_set = current_right_set.copy()

    # Return the best cut
    return best_left_set, best_right_set


def cheeger_trevisan_cut(graph):
    """Given a networkx graph G, find the almost-bipartite set given by the Cheeger-Trevisan algorithm.

    :param graph: The graph on which to operate.
    :return: Two sets containing the vertices on each side of the cut
    """
    # Compute the key graph matrices
    adjacency_matrix = nx.adjacency_matrix(graph)
    laplacian_matrix = nx.normalized_laplacian_matrix(graph)
    graph_degrees = [t[1] for t in nx.degree(graph)]

    # Compute the second smallest eigenvalue of the laplacian matrix
    _, top_eigenvector = sp.sparse.linalg.eigsh(laplacian_matrix, which="LM", k=1)
    top_eigenvector = top_eigenvector[:, 0]

    # Perform the sweep cut and return
    left_set, right_set = two_sided_sweep(adjacency_matrix, top_eigenvector, graph_degrees)
    return left_set, right_set
