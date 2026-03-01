import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math
from heapq import heappush, heappop
from collections import defaultdict

COLOR_BG = "#1e1e2e"
COLOR_GRID = "#2f2f4a"
COLOR_START = "#00d26a"
COLOR_GOAL = "#ff5555"
COLOR_WALL = "#6272a4"
COLOR_OPEN = "#ffb86c" # frontier / open set
COLOR_CLOSED = "#44475a" # visited / closed
COLOR_PATH = "#50fa7b"
COLOR_TEXT = "#f8f8f2"
COLOR_PANEL = "#282a36"

class DynamicPathfinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic A*/Greedy Pathfinding")
        self.root.configure(bg=COLOR_BG)
        # ── Default parameters ───────────────────────
        self.rows = 30
        self.cols = 40
        self.cell_size = 22
        self.obstacle_prob = 0.28 # ~28% walls at start
        self.dynamic_spawn_prob = 0.008 # per free cell per step
        self.start = (2, 2)
        self.goal = None # will be set to bottom-right
        self.grid = None
        self.canvas = None
        self.cells = None
        self.algorithm = tk.StringVar(value="A*")
        self.heuristic = tk.StringVar(value="Manhattan")
        self.dynamic_mode = tk.BooleanVar(value=False)
        self.running = False
        self.paused = False
        self.speed_ms = 40
        self.create_gui()
        self.new_maze()
    # ────────────────────────────────────────────────
    # GUI Layout
    # ────────────────────────────────────────────────
    def create_gui(self):
        top = tk.Frame(self.root, bg=COLOR_PANEL, padx=10, pady=8)
        top.pack(fill=tk.X)
        # Left controls
        left = tk.Frame(top, bg=COLOR_PANEL)
        left.pack(side=tk.LEFT, padx=10)
        tk.Label(left, text="Rows:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=0, column=0, sticky="e")
        self.ent_rows = tk.Entry(left, width=6, justify="center")
        self.ent_rows.insert(0, str(self.rows))
        self.ent_rows.grid(row=0, column=1, padx=4)
        tk.Label(left, text="Cols:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=1, column=0, sticky="e")
        self.ent_cols = tk.Entry(left, width=6, justify="center")
        self.ent_cols.insert(0, str(self.cols))
        self.ent_cols.grid(row=1, column=1, padx=4)
        tk.Button(left, text="New Maze", command=self.new_maze,
                  bg="#44475a", fg=COLOR_TEXT, activebackground="#6272a4").grid(row=2, column=0, columnspan=2, pady=6)
        # Middle controls
        mid = tk.Frame(top, bg=COLOR_PANEL)
        mid.pack(side=tk.LEFT, padx=20)
        tk.Label(mid, text="Algorithm:", bg=COLOR_PANEL, fg=COLOR_TEXT).pack()
        ttk.Combobox(mid, textvariable=self.algorithm, values=["A*", "Greedy"], state="readonly", width=12).pack()
        tk.Label(mid, text="Heuristic:", bg=COLOR_PANEL, fg=COLOR_TEXT).pack()
        ttk.Combobox(mid, textvariable=self.heuristic, values=["Manhattan", "Euclidean"], state="readonly", width=12).pack(pady=4)
        tk.Checkbutton(mid, text="Dynamic obstacles", variable=self.dynamic_mode,
                       bg=COLOR_PANEL, fg=COLOR_TEXT, selectcolor="#44475a").pack(anchor="w")
        # Right controls
        right = tk.Frame(top, bg=COLOR_PANEL)
        right.pack(side=tk.RIGHT, padx=10)
        self.btn_start = tk.Button(right, text="Start / Replan", command=self.start_search,
                                   bg="#50fa7b", fg="black", font=("Segoe UI",10,"bold"), width=14)
        self.btn_start.pack(pady=3)
        self.btn_pause = tk.Button(right, text="Pause", command=self.toggle_pause,
                                   bg="#ffb86c", fg="black", width=14, state="disabled")
        self.btn_pause.pack(pady=3)
        self.btn_clear_path = tk.Button(right, text="Clear Path Only", command=self.clear_path,
                                        bg="#6272a4", fg=COLOR_TEXT, width=14)
        self.btn_clear_path.pack(pady=3)
        # Status bar
        self.status = tk.Label(self.root, text="Ready", bg=COLOR_BG, fg="#6272a4", anchor="w")
        self.status.pack(fill=tk.X, padx=10, pady=(0,4))
        # Canvas
        self.canvas_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.canvas = tk.Canvas(self.canvas_frame, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(expand=True)
        # Metrics
        self.metrics_frame = tk.Frame(self.root, bg=COLOR_PANEL)
        self.metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        self.lbl_nodes = tk.Label(self.metrics_frame, text="Nodes expanded: 0", bg=COLOR_PANEL, fg=COLOR_TEXT)
        self.lbl_nodes.pack(side=tk.LEFT, padx=20)
        self.lbl_length = tk.Label(self.metrics_frame, text="Path length: —", bg=COLOR_PANEL, fg=COLOR_TEXT)
        self.lbl_length.pack(side=tk.LEFT, padx=20)
        self.lbl_time = tk.Label(self.metrics_frame, text="Time: — ms", bg=COLOR_PANEL, fg=COLOR_TEXT)
        self.lbl_time.pack(side=tk.LEFT, padx=20)
    def resize_canvas(self):
        w = self.cols * self.cell_size + 4
        h = self.rows * self.cell_size + 4
        self.canvas.config(width=w, height=h)
        self.canvas.delete("all")
    def new_maze(self):
        try:
            r = int(self.ent_rows.get())
            c = int(self.ent_cols.get())
            if not (8 <= r <= 80 and 8 <= c <= 120):
                raise ValueError
            self.rows, self.cols = r, c
        except:
            messagebox.showwarning("Invalid size", "Rows/Cols should be 8–80 / 8–120")
            return
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # Random obstacles
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < self.obstacle_prob:
                    self.grid[i][j] = 1
        # Force start & goal free
        self.start = (1, 1)
        self.goal = (self.rows-2, self.cols-2)
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.goal[0]][self.goal[1]] = 0
        self.resize_canvas()
        self.cells = [[None]*self.cols for _ in range(self.rows)]
        self.draw_grid()
        self.clear_path()
        self.status.config(text=f"New {self.rows}×{self.cols} maze created", fg="#50fa7b")
    def draw_grid(self):
        self.canvas.delete("grid")
        cs = self.cell_size
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j*cs+2, i*cs+2
                x2, y2 = x1+cs-1, y1+cs-1
                fill = COLOR_WALL if self.grid[i][j] else COLOR_GRID
                tag = f"cell_{i}_{j}"
                self.cells[i][j] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=fill, outline="#44475a", tags=("grid",tag))
        # Start & Goal
        self.paint_cell(self.start, COLOR_START, "start")
        self.paint_cell(self.goal, COLOR_GOAL, "goal")
    def paint_cell(self, pos, color, tag=None):
        if not pos: return
        i,j = pos
        if 0 <= i < self.rows and 0 <= j < self.cols:
            self.canvas.itemconfig(f"cell_{i}_{j}", fill=color)
            if tag:
                self.canvas.addtag_withtag(tag, f"cell_{i}_{j}")
    # ────────────────────────────────────────────────
    # Heuristics
    # ────────────────────────────────────────────────
    def h(self, a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        if self.heuristic.get() == "Manhattan":
            return dx + dy
        else: # Euclidean
            return math.hypot(dx, dy)
    # ────────────────────────────────────────────────
    # A* / Greedy Best-First
    # ────────────────────────────────────────────────
    def search(self):
        if self.running: return
        alg = self.algorithm.get()
        self.clear_path(keep_walls=True)
        came_from = {}
        g_score = defaultdict(lambda: float('inf'))
        g_score[self.start] = 0
        if alg == "A*":
            f_score = defaultdict(lambda: float('inf'))
            f_score[self.start] = self.h(self.start, self.goal)
            open_set = [(f_score[self.start], id(self.start), self.start)] # tie-breaker with id
        else: # Greedy
            open_set = [(self.h(self.start, self.goal), id(self.start), self.start)]
        closed = set()
        nodes_expanded = 0
        directions = [(-1,0),(1,0),(0,-1),(0,1)] # 4-way
        start_time = time.perf_counter()
        self.running = True
        self.btn_start.config(state="disabled")
        self.btn_pause.config(state="normal", text="Pause")
        while open_set and self.running:
            if self.paused:
                self.root.after(50, self.search) # continue polling
                return
            _, _, current = heappop(open_set)
            if current in closed: continue
            closed.add(current)
            nodes_expanded += 1
            # Paint frontier (approximation - only current open set visualization is heavy)
            # We paint closed nodes instead (cheaper & still informative)
            self.paint_cell(current, COLOR_CLOSED)
            if current == self.goal:
                # reconstruct path
                path = []
                cur = current
                while cur != self.start:
                    path.append(cur)
                    cur = came_from.get(cur)
                    if cur is None: break
                path.append(self.start)
                path.reverse()
                path_len = len(path)-1
                elapsed = (time.perf_counter() - start_time)*1000
                self.show_path(path)
                self.lbl_nodes.config(text=f"Nodes expanded: {nodes_expanded:,}")
                self.lbl_length.config(text=f"Path length: {path_len}")
                self.lbl_time.config( text=f"Time: {elapsed:.1f} ms")
                self.status.config(text=f"Found path (len={path_len})", fg=COLOR_PATH)
                self.finish_search()
                return
            for di, dj in directions:
                ni, nj = current[0] + di, current[1] + dj
                if not (0 <= ni < self.rows and 0 <= nj < self.cols):
                    continue
                if self.grid[ni][nj] == 1:
                    continue # wall
                tentative_g = g_score[current] + 1
                if tentative_g < g_score[(ni,nj)]:
                    came_from[(ni,nj)] = current
                    g_score[(ni,nj)] = tentative_g
                    if alg == "A*":
                        f_new = tentative_g + self.h((ni,nj), self.goal)
                        f_score[(ni,nj)] = f_new
                        heappush(open_set, (f_new, id((ni,nj)), (ni,nj)))
                    else:
                        h_val = self.h((ni,nj), self.goal)
                        heappush(open_set, (h_val, id((ni,nj)), (ni,nj)))
            # Small delay for animation
            self.root.update()
            self.root.after(self.speed_ms)
        # No path
        if self.running:
            self.status.config(text="No path found", fg="#ff5555")
            self.finish_search()
    def show_path(self, path):
        for i, pos in enumerate(path):
            if pos == self.start or pos == self.goal:
                continue
            self.paint_cell(pos, COLOR_PATH, "path")
    def finish_search(self):
        self.running = False
        self.paused = False
        self.btn_start.config(state="normal")
        self.btn_pause.config(state="disabled", text="Pause")
    def toggle_pause(self):
        if not self.running: return
        self.paused = not self.paused
        self.btn_pause.config(text="Continue" if self.paused else "Pause")
    def clear_path(self, keep_walls=False):
        self.canvas.delete("path")
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    continue
                if (i,j) == self.start:
                    self.paint_cell((i,j), COLOR_START)
                elif (i,j) == self.goal:
                    self.paint_cell((i,j), COLOR_GOAL)
                else:
                    if not keep_walls:
                        self.paint_cell((i,j), COLOR_GRID)
        self.lbl_nodes.config(text="Nodes expanded: —")
        self.lbl_length.config(text="Path length: —")
        self.lbl_time.config(text="Time: — ms")
    def start_search(self):
        if self.running:
            # Re-plan
            self.clear_path(keep_walls=True)
            self.running = False
            self.paused = False
            self.root.after(100, self.search)
        else:
            self.search()
    # ────────────────────────────────────────────────
    # Dynamic mode – spawn obstacles during movement
    # ────────────────────────────────────────────────
    def dynamic_step(self):
        if not self.running or not self.dynamic_mode.get():
            return
        added = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 0 and (i,j) != self.start and (i,j) != self.goal:
                    if random.random() < self.dynamic_spawn_prob:
                        self.grid[i][j] = 1
                        self.paint_cell((i,j), COLOR_WALL)
                        added += 1
        if added > 0:
            self.status.config(text=f"{added} new obstacle(s) appeared — replanning...", fg="#ffb86c")
            self.root.after(400, self.start_search) # replan soon
        else:
            self.root.after(200, self.dynamic_step)
    # ────────────────────────────────────────────────
    # Mouse click → toggle wall
    # ────────────────────────────────────────────────
    def on_click(self, event):
        if self.running: return
        cs = self.cell_size
        j = (event.x - 2) // cs
        i = (event.y - 2) // cs
        if not (0 <= i < self.rows and 0 <= j < self.cols):
            return
        if (i,j) == self.start or (i,j) == self.goal:
            return
        self.grid[i][j] ^= 1 # toggle
        col = COLOR_WALL if self.grid[i][j] else COLOR_GRID
        self.paint_cell((i,j), col)
# ────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicPathfinder(root)
    # Bind mouse click for manual wall editing
    app.canvas.bind("<Button-1>", app.on_click)
    # Start dynamic timer
    def dynamic_loop():
        app.dynamic_step()
        root.after(350, dynamic_loop)
    root.after(1000, dynamic_loop)
    root.mainloop()