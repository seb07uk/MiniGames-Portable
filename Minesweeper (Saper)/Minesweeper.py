import tkinter as tk
from tkinter import messagebox
import random

LEVELS = {
    "Easy": {"size": 8, "mines": 10},
    "Medium": {"size": 10, "mines": 15},
    "Hard": {"size": 12, "mines": 25}
}

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_mine = False
        self.flagged = False
        self.revealed = False
        self.neighbor_mines = 0

class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.level = "Medium"
        self.time = 0
        self.timer_id = None
        self.create_menu()
        self.restart_game()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        for level in LEVELS:
            game_menu.add_command(label=level, command=lambda l=level: self.change_level(l))
        menu.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        messagebox.showinfo("About", "polsoft.ITS London\n\nMinesweeper v1.0\n\nCopyright 2025© Sebastian Januchowski")

    def change_level(self, level):
        self.level = level
        self.restart_game()

    def restart_game(self):
        if hasattr(self, "frame"):
            self.frame.destroy()
        if hasattr(self, "time_label"):
            self.time_label.destroy()
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.size = LEVELS[self.level]["size"]
        self.mine_count = LEVELS[self.level]["mines"]
        self.board = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]
        self.place_mines()
        self.calculate_neighbors()
        self.time = 0
        self.time_label = tk.Label(self.root, text="Time: 0 s", font=("Arial", 12))
        self.time_label.pack()
        self.update_time()
        self.create_interface()

    def update_time(self):
        self.time += 1
        self.time_label.config(text=f"Time: {self.time} s")
        self.timer_id = self.root.after(1000, self.update_time)

    def place_mines(self):
        mines = 0
        while mines < self.mine_count:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if not self.board[x][y].has_mine:
                self.board[x][y].has_mine = True
                mines += 1

    def calculate_neighbors(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y].has_mine:
                    continue
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            if self.board[nx][ny].has_mine:
                                count += 1
                self.board[x][y].neighbor_mines = count

    def create_interface(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for x in range(self.size):
            for y in range(self.size):
                btn = tk.Button(self.frame, width=2, height=1, font=("Arial", 12),
                                command=lambda x=x, y=y: self.reveal_cell(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.toggle_flag(x, y))
                btn.grid(row=x, column=y)
                self.buttons[x][y] = btn

    def reveal_cell(self, x, y):
        cell = self.board[x][y]
        if cell.revealed or cell.flagged:
            return
        cell.revealed = True
        btn = self.buttons[x][y]
        if cell.has_mine:
            btn.config(text="💣", bg="red")
            self.end_game(False)
        else:
            btn.config(text=str(cell.neighbor_mines) if cell.neighbor_mines > 0 else "", bg="lightgrey")
            if cell.neighbor_mines == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            self.reveal_cell(nx, ny)
        self.check_win()

    def toggle_flag(self, x, y):
        cell = self.board[x][y]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged
        btn = self.buttons[x][y]
        btn.config(text="🚩" if cell.flagged else "")

    def check_win(self):
        for x in range(self.size):
            for y in range(self.size):
                cell = self.board[x][y]
                if not cell.has_mine and not cell.revealed:
                    return
        self.end_game(True)

    def end_game(self, won):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        for x in range(self.size):
            for y in range(self.size):
                cell = self.board[x][y]
                btn = self.buttons[x][y]
                if cell.has_mine:
                    btn.config(text="💣", bg="red")
        message = "You won!" if won else "You lost!"
        result = tk.Label(self.root, text=f"{message} Time: {self.time} s", font=("Arial", 14), fg="blue")
        result.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()