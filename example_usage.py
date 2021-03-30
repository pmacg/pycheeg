import networkx as nx
import cheeger_cut


def main():
    # Construct an example graph
    G = nx.barbell_graph(10, 1)
    print(f"Sparse cut is: {cheeger_cut.cheeger_cut(G)}")


if __name__ == "__main__":
    main()