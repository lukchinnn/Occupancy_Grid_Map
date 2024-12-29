import heapq
import time
from .utils import get_neighbors, reconstruct_path

def run_dijkstra(start, goal, grid, rows, cols, draw_callback):
    """
    Parameters:
    - start: Tuple (row, col)
    - goal: Tuple (row, col) 
    - grid: 2D list representing the grid.
    - rows: Number of rows in the grid.
    - cols: Number of columns in the grid.
    - draw_callback: Function to redraw the grid after each step for visualization.

    Returns:
    - None.
    """
    if not start or not goal:
        print("Start or goal not set")
        return

    print(f"Running Dijkstra from {start} to {goal}")

    # Priority queue for nodes to be explored
    open_set = []
    heapq.heappush(open_set, (0, start))  # (cost, node)
    came_from = {}  
    cost_so_far = {start: 0}  # Cost from start to this node

    while open_set:
        current_cost, current = heapq.heappop(open_set)

        # If the goal is reached, reconstruct and highlight the path
        if current == goal:
            reconstruct_path(came_from, current, grid, highlight=True)
            draw_callback()
            return

        # Explore neighbors
        for neighbor in get_neighbors(current, rows, cols, grid):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(open_set, (new_cost, neighbor))
                if neighbor != goal:
                    # Mark the cell as visited (blue)
                    r, c = neighbor
                    grid[r][c] = 2
                    draw_callback()
                    time.sleep(0.01)

    print("No path found")
