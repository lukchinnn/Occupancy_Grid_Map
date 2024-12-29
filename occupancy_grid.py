import tkinter as tk
import random
from tkinter import filedialog
from algorithm import *


class OccupancyGrid:
    """
    A GUI for visualizing pathfinding algorithms.
    Can interact with the grid to set start and goal points,
    generate random obstacles, and run various algorithms to find paths.
    """

    def __init__(self, root):
        """
        Parameters:
        - root: The Tkinter root window
        """
        self.root = root
        self.root.title("Pathfinding Visualizer")

        # Fullscreen mode
        self.root.attributes("-fullscreen", True)

        # Grid dimensions
        self.rows = 100
        self.cols = 100
        self.cell_size = 10

        self.start = None
        self.goal = None

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # Create a canvas to display the grid
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Frame for control buttons
        frame = tk.Frame(root)
        frame.pack()

        # Add buttons for algorithms and maps
        tk.Button(frame, text="A*", command=self.run_astar).grid(row=0, column=0)
        tk.Button(frame, text="Dijkstra", command=self.run_dijkstra).grid(row=0, column=1)
        tk.Button(frame, text="RRT", command=self.run_rrt).grid(row=0, column=2)
        tk.Button(frame, text="Import PGM", command=self.import_pgm).grid(row=0, column=3)
        tk.Button(frame, text="Generate Random", command=self.generate_random_map).grid(row=0, column=4)

        # Status bar for feedback
        self.status_label = tk.Label(root, text="Welcome! Left-click to set Start, Right-click to set Goal.",
                                     bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Clicks to set the start and goal points
        self.canvas.bind("<Button-1>", self.set_start)  # Left-click sets the start point
        self.canvas.bind("<Button-3>", self.set_goal)  # Right-click sets the goal point

        # Keyboard shortcuts for common actions
        self.root.bind("<Escape>", self.toggle_fullscreen)  # Toggle fullscreen with Esc
        self.root.bind("r", lambda e: self.generate_random_map())  # 'r' to reset and generate a random map
        self.root.bind("a", lambda e: self.run_astar())  # 'a' to run A*
        self.root.bind("d", lambda e: self.run_dijkstra())  # 'd' to run Dijkstra
        self.root.bind("t", lambda e: self.run_rrt())  # 't' to run RRT

        self.draw_grid()

    def draw_grid(self):
        """
        Draws the grid on the canvas, updating colors for each cell
        """
        self.canvas.delete("all")  # Clear the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_size = min(width // self.cols, height // self.rows)

        for r in range(self.rows):
            for c in range(self.cols):
                color = "white"  # Free space
                if self.grid[r][c] == 1:
                    color = "black"  # Obstacle
                elif (r, c) == self.start:
                    color = "green"  # Start point
                elif (r, c) == self.goal:
                    color = "red"  # Goal point
                elif self.grid[r][c] == 2:
                    color = "blue"  # Visited cells
                elif self.grid[r][c] == 3:
                    color = "yellow"  # Final path
                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size,
                    (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                    fill=color, outline="gray"
                )
        self.root.update()

    def set_start(self, event):
        """
        Sets the start point on the grid
        """
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if self.grid[row][col] == 0: 
            self.start = (row, col)
            self.update_status(f"Start point set at {self.start}. Now set the Goal.")
            self.draw_grid()

    def set_goal(self, event):
        """
        Sets the goal point on the grid
        """
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if self.grid[row][col] == 0:  
            self.goal = (row, col)
            self.update_status(f"Goal point set at {self.goal}. Select an algorithm to run.")
            self.draw_grid()

    def generate_random_map(self):
        """
        Generates a random map with Probability = 0.2
        """
        self.grid = [[1 if random.random() < 0.2 else 0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.goal = None
        self.update_status("Random map generated. Set Start and Goal points.")
        self.draw_grid()

    def import_pgm(self):
        """
        Imports a PGM file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("PGM files", "*.pgm")])
        if not file_path:
            self.update_status("PGM import canceled.")
            return

        try:
            with open(file_path, 'rb') as file:
                header = file.readline().decode('ascii').strip()
                if header not in ["P2", "P5"]:
                    print("Unsupported PGM format")
                    return

                def read_non_comment_line():
                    while True:
                        line = file.readline().decode('ascii').strip()
                        if line and not line.startswith('#'):
                            return line

                dimensions = read_non_comment_line()
                width, height = map(int, dimensions.split())
                max_value = int(read_non_comment_line())

                grid_data = []
                if header == "P2":  # ASCII PGM
                    for line in file:
                        grid_data.extend(map(int, line.decode('ascii').split()))
                elif header == "P5":  # Binary PGM
                    grid_data = list(file.read())

                self.rows = height
                self.cols = width
                self.grid = [[0 if grid_data[r * self.cols + c] > max_value // 2 else 1 for c in range(self.cols)] for r in range(self.rows)]
                self.start = None
                self.goal = None
                self.update_status("PGM map imported. Set Start and Goal points.")
                self.draw_grid()
        except Exception as e:
            print(f"Error importing PGM file: {e}")
            self.update_status("Error importing PGM file.")

    def run_astar(self):
        """
        Runs the A* algorithm
        """
        if not self.start or not self.goal:
            self.update_status("Start or Goal not set. Set both points before running A*.")
            return

        visited_cells = 0

        def update_with_visits():
            nonlocal visited_cells
            visited_cells += 1
            if visited_cells % 50 == 0:
                self.update_status(f"A*: Visiting {visited_cells} cells...")

        run_astar(self.start, self.goal, self.grid, self.rows, self.cols, lambda: (self.draw_grid(), update_with_visits()))
        self.update_status(f"A* algorithm completed. Total visited cells: {visited_cells}.")

    def run_dijkstra(self):
        """
        Runs Dijkstra's algorithm
        """
        if not self.start or not self.goal:
            self.update_status("Start or Goal not set. Set both points before running Dijkstra.")
            return

        visited_cells = 0

        def update_with_visits():
            nonlocal visited_cells
            visited_cells += 1
            if visited_cells % 50 == 0:
                self.update_status(f"Dijkstra: Visiting {visited_cells} cells...")

        run_dijkstra(self.start, self.goal, self.grid, self.rows, self.cols, lambda: (self.draw_grid(), update_with_visits()))
        self.update_status(f"Dijkstra's algorithm completed. Total visited cells: {visited_cells}.")

    def run_rrt(self):
        """
        Runs the RRT algorithm
        """
        if not self.start or not self.goal:
            self.update_status("Start or Goal not set. Set both points before running RRT.")
            return

        visited_cells = 0

        def update_with_visits():
            nonlocal visited_cells
            visited_cells += 1
            if visited_cells % 50 == 0:
                self.update_status(f"RRT: Visiting {visited_cells} cells...")

        run_rrt(self.start, self.goal, self.grid, self.rows, self.cols, lambda: (self.draw_grid(), update_with_visits()))
        self.update_status(f"RRT algorithm completed. Total visited cells: {visited_cells}.")

    def toggle_fullscreen(self, event=None):
        """
        Toggles fullscreen mode.
        """
        is_fullscreen = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fullscreen)

    def update_status(self, message):
        """
        Updates the status bar

        Parameters:
        - message: A string containing the status message.
        """
        self.status_label.config(text=message)


if __name__ == "__main__":
    root = tk.Tk()
    app = OccupancyGrid(root)
    root.mainloop()
