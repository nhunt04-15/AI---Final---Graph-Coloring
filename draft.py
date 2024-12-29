import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def create_random_undirected_graph(num_nodes, num_edges):
    if num_edges < num_nodes - 1:
        raise ValueError("Số lượng cạnh phải ít nhất bằng số node - 1 để đảm bảo kết nối.")
    if num_edges > num_nodes * (num_nodes - 1) / 2:
        raise ValueError("Số lượng cạnh quá lớn cho số node đã cho.")
    G = nx.Graph()
    nodes = list(range(num_nodes))
    random.shuffle(nodes)
    for i in range(1, num_nodes):
        u = nodes[i - 1]
        v = nodes[i]
        G.add_edge(u, v)
    while G.number_of_edges() < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v)
    return G

def is_safe(graph, colors, node, color):
    for neighbor in graph.neighbors(node):
        if colors[neighbor] == color:
            return False
    return True

def draw_graph(graph, colors, canvas, pos):
    plt.clf()
    nx.draw(graph, pos, with_labels=True, node_color=[colors[node] for node in graph.nodes], edge_color='black', node_size=500, font_color='white', linewidths=2, edgecolors='black', node_shape='o')
    for node in graph.nodes:
        circle = plt.Circle(pos[node], radius=0.05, edgecolor='black', facecolor='none', linewidth=2)
        plt.gca().add_patch(circle)
    canvas.draw()

def graph_coloring(graph, num_colors, colors, node, canvas, pos, explanation_label, root):
    if node == len(graph.nodes):
        return True
    for color in range(1, num_colors + 1):
        if is_safe(graph, colors, node, color):
            colors[node] = color
            explanation_label.config(text=f"Coloring node {node} with color {color}")
            draw_graph(graph, colors, canvas, pos)
            root.update()
            root.after(1000, lambda: graph_coloring(graph, num_colors, colors, node + 1, canvas, pos, explanation_label, root))
            return True
    return False

def solve_graph_coloring(graph, canvas, pos, explanation_label, root):
    num_nodes = len(graph.nodes)
    for num_colors in range(1, num_nodes + 1):
        colors = [-1] * num_nodes
        if graph_coloring(graph, num_colors, colors, 0, canvas, pos, explanation_label, root):
            return

def main():
    root = tk.Tk()
    root.title("Graph Coloring Visualization")

    graph_frame = tk.Frame(root)
    graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    explanation_label = tk.Label(root, text="Starting graph coloring...")
    explanation_label.pack(side=tk.BOTTOM)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    num_nodes = 10
    num_edges = 15
    graph = create_random_undirected_graph(num_nodes, num_edges)
    pos = nx.spring_layout(graph)

    draw_graph(graph, [-1] * num_nodes, canvas, pos)
    root.after(1000, lambda: solve_graph_coloring(graph, canvas, pos, explanation_label, root))

    root.mainloop()

if __name__ == "__main__":
    main()
