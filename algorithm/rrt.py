import random
import time
from .utils import euclidean_distance, reconstruct_path

def run_rrt(start, goal, grid, rows, cols, draw_callback):
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

    print(f"Running RRT from {start} to {goal}")

    # Initialize the tree with the start node
    tree = {start: None}

    for _ in range(5000):
        # Generate a random point in the grid
        random_point = (random.randint(0, rows - 1), random.randint(0, cols - 1))

        # Find the nearest node in the tree to the random point
        nearest = min(tree.keys(), key=lambda n: euclidean_distance(n, random_point))

        # Move one step in the direction of the random point
        direction = ((random_point[0] - nearest[0]), (random_point[1] - nearest[1]))
        step = (nearest[0] + (1 if direction[0] > 0 else -1 if direction[0] < 0 else 0),
                nearest[1] + (1 if direction[1] > 0 else -1 if direction[1] < 0 else 0))

        # Make sure the step is within bounds and not on an obstacle
        if 0 <= step[0] < rows and 0 <= step[1] < cols and grid[step[0]][step[1]] == 0:
            tree[step] = nearest

            # If the goal is reached, reconstruct and highlight the path
            if step == goal:
                reconstruct_path(tree, step, grid, highlight=True)
                draw_callback()
                return

            # Mark the cell as visited (blue)
            r, c = step
            grid[r][c] = 2
            draw_callback()
            time.sleep(0.01)

    print("No path found")
