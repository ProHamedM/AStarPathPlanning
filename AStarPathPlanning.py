# Importing the heapq library to use a priority queue
import heapq

# Node class represents each point in the graph
class Node:
    def __init__(self, name, position=None):
        self.name = name
        self.adjacents = {}  # Dictionary of neighbor nodes and edge weights
        self.position = position  # (row, col) coordinates for heuristic calculation

    # Add a neighboring node with an associated weight
    def add_neighbor(self, neighbor, weight):
        self.adjacents[neighbor] = weight

    # Less than method to compare nodes in the priority queue
    def __lt__(self, other):
        return self.name < other.name

# Graph class to manage the network of nodes
class Graph:
    def __init__(self):
        self.nodes = {}

    # Adds a new node to the graph if it doesn't exist
    def add_node(self, name, position=None):
        if name not in self.nodes:
            self.nodes[name] = Node(name, position)

    # Creates an undirected edge between two nodes with a weight
    def add_edge(self, from_node, to_node, weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.nodes[from_node].add_neighbor(self.nodes[to_node], weight)
        self.nodes[to_node].add_neighbor(self.nodes[from_node], weight)  # Undirected graph

    # A* search algorithm to find the shortest path from start to end using heuristic
    def a_star(self, start_name, end_name):
        def heuristic(n1, n2):
            x1, y1 = self.nodes[n1].position
            x2, y2 = self.nodes[n2].position
            return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance

        open_set = [(0, self.nodes[start_name])]
        g_scores = {node: float('inf') for node in self.nodes}
        g_scores[start_name] = 0
        came_from = {node: None for node in self.nodes}

        while open_set:
            _, current_node = heapq.heappop(open_set)

            if current_node.name == end_name:
                break

            for neighbor, weight in current_node.adjacents.items():
                tentative_g = g_scores[current_node.name] + weight
                if tentative_g < g_scores[neighbor.name]:
                    came_from[neighbor.name] = current_node.name
                    g_scores[neighbor.name] = tentative_g
                    f_score = tentative_g + heuristic(neighbor.name, end_name)
                    heapq.heappush(open_set, (f_score, neighbor))

        # Reconstruct path
        path_result = []
        current = end_name
        while current is not None:
            path_result.insert(0, current)
            current = came_from[current]

        return path_result, g_scores[end_name]

# Simulated scenario: Robot lawnmower navigating a yard with A* search
if __name__ == "__main__":
    graph = Graph()

    # Representing a 5x5 yard grid as nodes (R1C1 = Row 1, Column 1)
    for row in range(1, 6):
        for col in range(1, 6):
            name = f"R{row}C{col}"
            graph.add_node(name, (row, col))

    # Connect adjacent yard cells
    for row in range(1, 6):
        for col in range(1, 6):
            current = f"R{row}C{col}"
            if col < 5:
                right = f"R{row}C{col+1}"
                graph.add_edge(current, right, 1)
            if row < 5:
                down = f"R{row+1}C{col}"
                graph.add_edge(current, down, 1)

    # Simulate mowing path from top-left to bottom-right using A*
    start = "R1C1"
    end = "R5C5"

    path_result, total_cost = graph.a_star(start, end)
    print(f"A* Robot lawnmower path from {start} to {end}: {path_result} with total cost: {total_cost}")