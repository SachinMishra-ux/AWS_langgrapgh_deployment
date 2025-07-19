# visualize_graph.py
from graph_builder import graph  # or build_graph()

def main():
    # Ensure your graph is compiled
    compiled = graph.compile() if hasattr(graph, "compile") else graph
    internal = compiled.get_graph()

    # ASCII view
    print("=== ASCII Diagram ===")
    internal.print_ascii()

if __name__ == "__main__":
    main()
