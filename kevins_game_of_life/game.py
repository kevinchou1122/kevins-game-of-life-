import tkinter as tk
from tkinter import filedialog

GRID_SIZE = 70
CELL_SIZE = 10

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.master.title("Game of Life")

        # Create canvas for drawing
        self.canvas = tk.Canvas(master, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg='white')
        self.canvas.pack()

        # Initialize empty grid
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Create control buttons
        self.control_frame = tk.Frame(master)
        self.control_frame.pack()

        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT)

        self.random_button = tk.Button(self.control_frame, text="load", command=self.load)
        self.random_button.pack(side=tk.LEFT)

        # Initialize simulation state
        self.running = False

        # Draw the initial grid
        self.draw_grid()

        # Bind click event to handle cell toggle
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_grid(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                fill_color = "black" if self.grid[row][col] else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")

    def handle_click(self, event):
        col=event.x//CELL_SIZE
        row=event.y//CELL_SIZE

        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.toggle_cell(row,col)

    def toggle_cell(self, row, col):
        self.grid[row][col]=1-self.grid[row][col]
        self.draw_grid()

    def count_neighbors(self, row, col):
        count=0
        for i in range(-1,2):
            for j in range(-1,2):
                if i==0 and j==0:
                    continue

                r=(row+i)%GRID_SIZE
                c=(col+j)%GRID_SIZE

                count+=self.grid[r][c]
        return count


    def update_grid(self):
        new_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        temp_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                current=self.grid[row][col]
                neighbors=self.count_neighbors(row,col)

                if current == 1:  # Live cell
                    if neighbors == 2 or neighbors == 3:
                        temp_grid[row][col] = 1
                    else:
                        temp_grid[row][col] = 0
                else:  # Dead cell
                    if neighbors == 3:  # Can become alive with 3 neighbors
                        temp_grid[row][col] = 1
                    else:
                        temp_grid[row][col] = 0

        self.grid = temp_grid
        self.draw_grid()

        if self.running:
            self.master.after(75, self.update_grid)




    def start_simulation(self):
        if not self.running:
            self.running = True
            self.update_grid()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_simulation(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)


    def clear_grid(self):
        self.stop_simulation()
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.draw_grid()

    def load(self):
        #the centering mechanic makes it kind of slow so be patient
        filename = filedialog.askopenfilename(defaultextension='.txt')

        if filename:
            with open(filename, 'r') as file:
                rowList = file.readlines()

            pattern_height=(len(rowList))
            pattern_width=(max(len(row) for row in rowList))

            start_row = (GRID_SIZE - pattern_height) // 2
            start_col = (GRID_SIZE - pattern_width) // 2

            self.clear_grid()

            for row in range(pattern_height):
                for col in range(pattern_width):
                    if rowList[row][col] in '01':
                        value=int(rowList[row][col])
                        grid_row = start_row + row
                        grid_col = start_col + col

                        if 0 <= grid_row < GRID_SIZE and 0 <= grid_col < GRID_SIZE:
                            self.grid[grid_row][grid_col] = value


                    self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
