import math

def heuristic(a, b):
    """
    Calculates the Manhattan distance between two points.
    Parameters:
    - a: Tuple (row, col) of the first point.
    - b: Tuple (row, col) of the second point.
    Returns:
    - Manhattan distance as an integer.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_distance(a, b):
    """
    Calculates the Euclidean distance between two points.
    Parameters:
    - a: Tuple (row, col) of the first point.
    - b: Tuple (row, col) of the second point.
    Returns:
    - Euclidean distance as a float.
    """
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_neighbors(node, rows, cols, grid):
    """
    Retrieves all valid neighbors of a given node in the grid.
    Parameters:
    - node: Tuple (row, col) of the current node.
    - rows: Number of rows in the grid.
    - cols: Number of columns in the grid.
    - grid: 2D list representing the grid.
    Returns:
    - List of neighbor nodes as tuples (row, col).
    """
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dr, dc in directions:
        nr, nc = node[0] + dr, node[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(came_from, current, grid, highlight=False):
    """
    Reconstructs the path from the start to the goal.

    Parameters:
    - came_from: Dictionary mapping each node to its parent.
    - current: Tuple (row, col) of the current node (goal).
    - grid: 2D list representing the grid.
    - highlight: Boolean, if True, marks the path in yellow.

    Returns:
    - None. Modifies the grid to display the path.
    """
    while current in came_from:
        r, c = current
        grid[r][c] = 3 if highlight else 2
        current = came_from[current]
