import networkx as nx
import pycheeg.cheeger
import pycheeg.cheeger_trevisan


def main():
    # Construct an example graph
    G = nx.barbell_graph(10, 1)
    print(f"Sparse cut is: {pycheeg.cheeger.cheeger_cut(G)}")
    print(f"Dense cut is: {pycheeg.cheeger_trevisan.cheeger_trevisan_cut(G)}")


if __name__ == "__main__":
    main()
