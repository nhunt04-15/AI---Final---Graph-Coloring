import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_random_undirected_graph(num_nodes, num_edges):
    """
    Tạo một đồ thị vô hướng ngẫu nhiên với số node, số cạnh cho trước
    - num_nodes: số lượng node;
    - num_edges: số lượng cạnh
    """
    if num_edges < num_nodes - 1:
        raise ValueError("Số lượng cạnh phải ít nhất bằng số node - 1 để đảm bảo kết nối.")

    if num_edges > num_nodes * (num_nodes - 1) / 2:
        raise ValueError("Số lượng cạnh quá lớn cho số node đã cho.")

    G = nx.Graph()
    # Tạo một cây khung để đảm bảo tất cả các node được kết nối
    nodes = list(range(num_nodes))
    random.shuffle(nodes)
    for i in range(1, num_nodes):
        u = nodes[i - 1]
        v = nodes[i]
        G.add_edge(u, v)

    # Add the remaining edges randomly
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

def graph_coloring(graph, num_colors, colors, node):
    if node == len(graph.nodes):
        return True

    for color in range(1, num_colors + 1):
        if is_safe(graph, colors, node, color):
            colors[node] = color
            if graph_coloring(graph, num_colors, colors, node + 1):
                return True
            colors[node] = -1

    return False

def solve_graph_coloring(graph):
    num_nodes = len(graph.nodes)
    for num_colors in range(1, num_nodes + 1):
        colors = [-1] * num_nodes
        if graph_coloring(graph, num_colors, colors, 0):
            return colors, num_colors
    return None, num_nodes

def visualize_graph(G, colors, canvas_frame):
    """
    Vẽ đồ thị tô màu
    """
    pos = nx.spring_layout(G)
    # Tô màu các node dựa trên màu sắc đã tính toán
    node_colors = [colors[node] for node in G]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.jet, node_size=700, font_size=12,
            font_weight='bold')

    # Hiển thị đồ thị trong cửa sổ Tkinter
    plt.title("Graph Visualization with Coloring")
    plt.axis('off')  # Tắt trục
    plt.show()

    # Embed the plot into tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Example usage
num_nodes = 10
num_edges = 15
G = create_random_undirected_graph(num_nodes, num_edges)

# Solve the graph coloring problem
colors, min_colors = solve_graph_coloring(G)

if colors:
    print(f"Graph coloring with {min_colors} colors: {colors}")
    visualize_graph(G, colors)
else:
    print("No solution found.")







