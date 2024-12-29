import heapq
import time
from .utils import heuristic, get_neighbors, reconstruct_path

def run_astar(start, goal, grid, rows, cols, draw_callback):
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

    print(f"Running A* from {start} to {goal}")

    # Priority queue for nodes to be explored
    open_set = []
    heapq.heappush(open_set, (0, start))  # (priority, node)
    came_from = {}  # Tracks the path
    g_score = {start: 0}  # Cost from start to this node
    f_score = {start: heuristic(start, goal)}  # Estimated total cost

    while open_set:
        _, current = heapq.heappop(open_set)

        # If the goal is reached, reconstruct and highlight the path
        if current == goal:
            reconstruct_path(came_from, current, grid, highlight=True)
            draw_callback()
            return

        # Explore neighbors
        for neighbor in get_neighbors(current, rows, cols, grid):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                if neighbor != goal:
                    # Mark the cell as visited (blue)
                    r, c = neighbor
                    grid[r][c] = 2
                    draw_callback()
                    time.sleep(0.01)

    print("No path found")
