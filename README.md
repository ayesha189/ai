# Dynamic A*/Greedy Pathfinding Visualizer

A real-time, interactive pathfinding visualizer built with Python and Tkinter.
Watch **A\*** and **Greedy Best-First Search** navigate a randomly generated maze — step by step, cell by cell — with live performance metrics, dynamic obstacles, and full mouse control.

---

## 1. Project Overview

**Dynamic A*/Greedy Pathfinding Visualizer** is a desktop application built using Python and the Tkinter GUI library. It provides an animated, interactive visualization of two classical AI search algorithms — **A* Search** and **Greedy Best-First Search** — operating on a randomly generated grid maze.

This tool makes algorithm behavior visible. Instead of reading about A* in a textbook, you watch it explore a grid in real time — expanding cells, evaluating costs, and tracing the shortest route from a green start node to a red goal node.

The application is suitable for students learning AI and algorithms, developers who want to understand pathfinding intuitively, and anyone building projects that involve grid-based navigation or autonomous movement.

---

## 2. Features

- **A\* Algorithm** — Optimal pathfinding using f(n) = g(n) + h(n); guarantees the shortest path
- **Greedy Best-First Search** — Fast heuristic-only search using h(n); does not guarantee optimality
- **Switchable Heuristics** — Manhattan and Euclidean distance, changeable at runtime
- **Dynamic Obstacles** — New walls spawn mid-search, triggering automatic replanning
- **Manual Wall Editing** — Left-click any cell to toggle walls on or off
- **Live Performance Metrics** — Nodes expanded, path length, and execution time
- **Customizable Grid** — Set rows (8–80) and columns (8–120)
- **Animated Visualization** — Step-by-step color-coded cell expansion

---

## 3. System Requirements

| Requirement | Specification |
|---|---|
| Python Version | 3.8 or higher |
| Tkinter Library | Included with Python — no installation needed |
| Operating System | Windows 10/11, macOS 10.14+, Ubuntu 18.04+ |
| RAM | 512 MB minimum (1 GB recommended for large grids) |
| Display | 1280 x 720 minimum resolution |
| External Packages | None — zero pip installs required |

> **Important:** All libraries used (`tkinter`, `heapq`, `collections`, `math`, `random`, `time`) are part of the Python Standard Library and ship with every Python installation.

---

## 4. Installation

### 4.1 Install Python

Download and install Python 3.8 or higher from the official Python website:
https://www.python.org/downloads/

- **Windows:** Check `"Add Python to PATH"` during installation before clicking Install Now.
- **macOS:** Python 3 can also be installed via Homebrew: `brew install python3`
- **Linux:** Python 3 is usually pre-installed. Verify with: `python3 --version`

### 4.2 Verify Tkinter

Confirm Tkinter is available by running the following in a terminal:

```bash
python -m tkinter
```

A small test window should appear. If it does, Tkinter is ready and no further setup is needed.

### 4.3 Tkinter on Linux (if missing)

```bash
# Ubuntu / Debian
sudo apt-get install python3-tk

# Fedora / RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

### 4.4 Download the Script

Save the file `dynamic_pathfinder.py` to any folder on your machine. No installation wizard, `setup.py`, or build step is required — the application runs directly as a single script.

---

## 5. How to Run

```bash
python dynamic_pathfinder.py
```

On systems where Python 3 is not the default:

```bash
python3 dynamic_pathfinder.py
```

The application window opens immediately. No compilation or build step is needed.

---

## 6. How to Use — Full Walkthrough

### 6.1 The Interface at a Glance

When you open the application, you will see the following elements:

| Element | Description |
|---|---|
| Dark grid | The maze area filling most of the window |
| Bright green cell (top-left) | The Start node |
| Red/pink cell (bottom-right) | The Goal node |
| Blue-gray cells | Walls and obstacles |
| Control panel (top) | Buttons, dropdowns, and settings |
| Metrics bar (bottom) | Nodes expanded, path length, execution time |

### 6.2 Running Your First Search

1. **Generate a maze.** Click **New Maze**. A fresh random grid is created with start and goal at opposite corners.
2. **Choose an algorithm.** Select `A*` for optimal shortest path, or `Greedy` for faster but potentially suboptimal search.
3. **Choose a heuristic.** Select `Manhattan` for standard 4-directional grids, or `Euclidean` for straight-line distance.
4. **Start the search.** Click **Start / Replan**. Cells turn dark gray as they are visited. When the goal is reached, a cyan path is drawn.
5. **Compare algorithms.** Click **Clear Path**, switch the algorithm, and run again on the same maze. Compare nodes expanded and path length.

### 6.3 Drawing Custom Mazes

You can design your own obstacle layout directly on the grid:

- **Left-click an empty cell** to turn it into a wall (blue-gray)
- **Left-click a wall cell** to remove it (returns to dark grid)
- Click and drag to draw entire barriers quickly
- The start and goal cells are protected — clicking on them does nothing

> **Tip:** Draw a narrow corridor that forces a long detour, then compare how A* and Greedy navigate it.

### 6.4 Using Dynamic Obstacles

**Dynamic mode** simulates a real-world scenario where the environment changes while the agent is navigating.

**To enable:** Check the **Dynamic obstacles** checkbox in the Algorithm Settings panel before starting the search.

What happens during the search:

- New walls randomly appear on free cells during execution
- The status bar shows: *"N new obstacle(s) appeared — replanning..."*
- The algorithm automatically restarts with the updated grid
- You watch it find an alternative path around the new blockage

> **Tip:** Enable Dynamic Obstacles on a large grid (40×60) with A* to see multiple replanning events in a single run.

### 6.5 Reading the Metrics

| Metric | What It Means |
|---|---|
| **Nodes expanded** | How many cells the algorithm evaluated. Lower = more efficient search. |
| **Path length** | Number of steps in the final path. A* always finds the minimum. |
| **Time (ms)** | Wall-clock time for the search, including animation overhead. |

> **Key insight:** On the same maze, A* and Greedy may find paths of different lengths. This is the core trade-off — **optimality versus speed**.

### 6.6 Color Legend

| Color | Meaning |
|---|---|
| Bright Green | Start node |
| Red / Pink | Goal node |
| Blue-Gray | Wall / obstacle |
| Dark Gray | Visited cell (closed set) |
| Cyan / Teal | Final path from start to goal |

### 6.7 Controls Quick Reference

| Input | Action |
|---|---|
| Left-click on empty cell | Add a wall |
| Left-click on wall cell | Remove the wall |
| **New Maze** button | Regenerate the entire grid randomly |
| **Start / Replan** button | Run the algorithm, or replan if mid-run |
| **Pause** button | Freeze the animation — click again to resume |
| **Clear Path** button | Remove path and visited colors, keep walls |

---

## 7. Using This Project in VS Code

### 7.1 Install VS Code

Download and install Visual Studio Code from:
https://code.visualstudio.com/

### 7.2 Install the Python Extension

1. Open VS Code
2. Press `Ctrl + Shift + X` (Windows/Linux) or `Cmd + Shift + X` (macOS) to open Extensions
3. Search for **Python** by Microsoft
4. Click **Install**

This extension provides syntax highlighting, IntelliSense autocomplete, linting, and the ability to run Python files directly from the editor.

### 7.3 Open the Project Folder

1. In VS Code, go to **File → Open Folder**
2. Navigate to and select the folder where you saved `dynamic_pathfinder.py`
3. The file appears in the **Explorer** panel on the left sidebar

### 7.4 Select Your Python Interpreter

1. Press `Ctrl + Shift + P` to open the **Command Palette**
2. Type `Python: Select Interpreter` and press Enter
3. Choose your Python 3.8+ installation from the dropdown

The selected interpreter appears in the bottom-left status bar of VS Code.

> **Note:** If Python does not appear in the list, ensure it was installed with `"Add Python to PATH"` enabled, then restart VS Code.

### 7.5 Run the Script

**Option A — Run Button (easiest):**
Open `dynamic_pathfinder.py` and click the **▷ Run Python File** button in the top-right corner. The app window launches immediately.

**Option B — Integrated Terminal:**
Press `` Ctrl + ` `` to open the VS Code terminal, then run:

```bash
python dynamic_pathfinder.py
```

**Option C — Debug Mode (F5):**
Press `F5` and select **Python File** as the debug configuration. The script runs with full breakpoint and variable inspection support.

### 7.6 Customizing the Code in VS Code

Key parameters you can tune to change application behavior:

| Parameter | Approx. Line | Default | Effect |
|---|---|---|---|
| `self.speed_ms` | 47 | `40` | Animation delay in ms. Lower = faster animation. |
| `self.obstacle_prob` | 44 | `0.28` | Wall density (0.1 = sparse, 0.5 = very dense) |
| `self.dynamic_spawn_prob` | 45 | `0.008` | How often new walls appear in dynamic mode |
| `self.rows` | 41 | `30` | Default grid rows on startup |
| `self.cols` | 42 | `40` | Default grid columns on startup |

**To change a value:** Click on the variable name and press `F2` to rename all occurrences, or edit the line directly and save with `Ctrl + S`.

### 7.7 Recommended VS Code Extensions

| Extension | Purpose |
|---|---|
| **Python** (Microsoft) | Core: syntax highlighting, IntelliSense, run and debug |
| **Pylance** | Faster type checking and smarter autocomplete |
| **Python Indent** | Correct auto-indentation for Python blocks |
| **Better Comments** | Color-coded comment annotations (TODO, NOTE, etc.) |
| **GitLens** | If you version-control this project with Git |

### 7.8 Optional Workspace Settings

Create a file at `.vscode/settings.json` inside your project folder:

```json
{
  "python.defaultInterpreterPath": "python",
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.formatOnSave": true,
  "files.trimTrailingWhitespace": true
}
```

### 7.9 Debugging Tips in VS Code

- Click to the left of any line number to set a **breakpoint** (a red dot appears)
- Press `F5` to run in debug mode — execution pauses at your breakpoint
- Inspect live variables in the **Variables** panel on the left sidebar
- Use the **Debug Console** to evaluate expressions like `g_score` or `open_set` mid-run
- **Good breakpoint location:** Inside the `while open_set` loop in `search()` to trace each expansion step

---

## 8. Project Structure

```
project-folder/
    dynamic_pathfinder.py    # Main application — single self-contained script
    README.md                # This documentation file
    .vscode/
        settings.json        # Optional VS Code workspace settings
```

---

## 9. Algorithm Notes

### 9.1 A* Search

A* selects the next node based on **f(n) = g(n) + h(n)**, where `g(n)` is the actual cost from the start and `h(n)` is the heuristic estimate to the goal. When the heuristic is admissible (never overestimates the true cost), A* is guaranteed to find the **optimal shortest path**.

### 9.2 Greedy Best-First Search

Greedy search expands nodes based on **h(n) only**, always moving toward what appears closest to the goal. This makes it faster in many cases but **does not guarantee the shortest path**. It can be misled by the heuristic and take longer routes or fail in dense mazes.

### 9.3 Heuristics

- **Manhattan Distance:** Calculates `|dx| + |dy|`. Best suited for 4-directional grid movement with no diagonal steps.
- **Euclidean Distance:** Calculates `sqrt(dx² + dy²)`. Straight-line distance. Slightly more aggressive in open spaces but marginally slower to compute.

---

## 10. Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'tkinter'` | Run `sudo apt-get install python3-tk` (Linux only) |
| `'python' is not recognized as a command` | Use `python3` instead, or add Python to your system PATH |
| Window opens but grid is blank | Resize the window manually to trigger a canvas redraw |
| VS Code shows "No interpreter selected" | Press `Ctrl+Shift+P` → Python: Select Interpreter |
| App does not launch from VS Code Run button | Ensure the Python extension is installed and an interpreter is selected |
| Slow animation on large grids | Reduce rows/cols, or set `self.speed_ms = 10` in the source |

---

## 11. Quick-Start Summary

1. **Install Python 3.8+** from https://www.python.org/downloads/
2. **Verify Tkinter** by running: `python -m tkinter`
3. **Save the file** `dynamic_pathfinder.py` to any folder
4. **Run:** `python dynamic_pathfinder.py`

> **No pip install required.** All dependencies are part of the Python Standard Library.

