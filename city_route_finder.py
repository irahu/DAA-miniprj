"""
========================================================
CITY ROUTE FINDER — Dijkstra's Shortest Path Algorithm
========================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import heapq          # For the priority queue (min-heap) used in Dijkstra
import math           # For drawing arrow/line positions


# ─────────────────────────────────────────────
#  1.  GRAPH DATA  (cities + roads + distances)
# ─────────────────────────────────────────────

# City positions on the canvas (x, y) — purely for drawing
CITY_POSITIONS = {
    "Delhi":     (370, 80),
    "Jaipur":    (180, 200),
    "Agra":      (460, 220),
    "Lucknow":   (600, 180),
    "Bhopal":    (340, 360),
    "Mumbai":    (160, 500),
    "Hyderabad": (380, 520),
    "Nagpur":    (450, 420),
    "Chennai":   (520, 610),
    "Bengaluru": (340, 640),
}

# Roads between cities with distances in km
# Format: (city_a, city_b, distance_km)
ROADS = [
    ("Delhi",     "Jaipur",    268),
    ("Delhi",     "Agra",      233),
    ("Delhi",     "Lucknow",   555),
    ("Jaipur",    "Agra",      238),
    ("Jaipur",    "Bhopal",    563),
    ("Agra",      "Lucknow",   363),
    ("Agra",      "Bhopal",    423),
    ("Lucknow",   "Nagpur",    695),
    ("Bhopal",    "Mumbai",    777),
    ("Bhopal",    "Nagpur",    357),
    ("Mumbai",    "Hyderabad", 711),
    ("Mumbai",    "Bengaluru", 981),
    ("Nagpur",    "Hyderabad", 503),
    ("Hyderabad", "Chennai",   626),
    ("Hyderabad", "Bengaluru", 570),
    ("Chennai",   "Bengaluru", 346),
]


# ─────────────────────────────────────────────
#  2.  BUILD ADJACENCY LIST  (graph structure)
# ─────────────────────────────────────────────

def build_graph(roads):
    """
    Convert the road list into an adjacency list.
    
    Example output:
        graph["Delhi"] = [("Jaipur", 268), ("Agra", 233), ("Lucknow", 555)]
    """
    graph = {city: [] for city in CITY_POSITIONS}
    for city_a, city_b, distance in roads:
        graph[city_a].append((city_b, distance))
        graph[city_b].append((city_a, distance))   # roads go both ways
    return graph


# ─────────────────────────────────────────────
#  3.  DIJKSTRA'S ALGORITHM
# ─────────────────────────────────────────────

def dijkstra(graph, start, end):
    """
    Find the shortest path from 'start' to 'end' using Dijkstra's Algorithm.

    Core idea:
        Always process the city with the SMALLEST known distance next.
        Use a Min-Heap (priority queue) to do this efficiently.

    Returns:
        (shortest_distance, path_list)
        e.g.  (1234, ["Delhi", "Agra", "Bhopal", "Nagpur"])
        Returns (infinity, []) if no path exists.
    """
    # Distance table — start with infinity for all cities
    distances = {city: math.inf for city in graph}
    distances[start] = 0

    # To reconstruct the path later, remember how we reached each city
    previous = {city: None for city in graph}

    # Min-heap: entries are (current_distance, city_name)
    heap = [(0, start)]

    visited = set()

    while heap:
        current_dist, current_city = heapq.heappop(heap)

        # Skip if we already found a better path to this city
        if current_city in visited:
            continue
        visited.add(current_city)

        # Early exit — we reached our destination
        if current_city == end:
            break

        # Explore all neighbours of the current city
        for neighbour, road_distance in graph[current_city]:
            if neighbour in visited:
                continue

            new_dist = current_dist + road_distance

            # If this new path is shorter, update
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                previous[neighbour] = current_city
                heapq.heappush(heap, (new_dist, neighbour))

    # ── Reconstruct path by tracing back through 'previous' ──
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    # If the path doesn't start at 'start', no route was found
    if path[0] != start:
        return math.inf, []

    return distances[end], path


# ─────────────────────────────────────────────
#  4.  TKINTER GUI APPLICATION
# ─────────────────────────────────────────────

class CityRouteFinder(tk.Tk):
    """Main application window."""

    # ── Colour palette ──
    BG          = "#0f1117"   # dark background
    CANVAS_BG   = "#161b27"   # map background
    ROAD_CLR    = "#2e3a50"   # normal road colour
    CITY_CLR    = "#3b82f6"   # default city dot
    HIGHLIGHT   = "#f59e0b"   # shortest-path road
    START_CLR   = "#22c55e"   # source city
    END_CLR     = "#ef4444"   # destination city
    PATH_CLR    = "#f59e0b"   # path city
    TEXT_CLR    = "#e2e8f0"
    PANEL_BG    = "#1e2535"
    BTN_BG      = "#3b82f6"
    BTN_FG      = "#ffffff"
    RESULT_BG   = "#0d1520"

    CITY_RADIUS = 14

    def __init__(self):
        super().__init__()
        self.title("City Route Finder — Dijkstra's Algorithm")
        self.configure(bg=self.BG)
        self.resizable(False, False)

        self.graph = build_graph(ROADS)

        self._setup_ui()
        self._draw_map()           # draw all roads + cities at start

    # ── UI layout ──────────────────────────────

    def _setup_ui(self):
        # ── Left panel (controls) ──
        panel = tk.Frame(self, bg=self.PANEL_BG, width=220, padx=16, pady=16)
        panel.pack(side=tk.LEFT, fill=tk.Y)
        panel.pack_propagate(False)

        tk.Label(panel, text="  City Route Finder",
                 font=("Courier", 13, "bold"),
                 bg=self.PANEL_BG, fg=self.TEXT_CLR).pack(pady=(0, 4))

        tk.Label(panel, text="Powered by Dijkstra's Algorithm",
                 font=("Courier", 8),
                 bg=self.PANEL_BG, fg="#64748b").pack(pady=(0, 16))

        # ── Source dropdown ──
        tk.Label(panel, text="FROM city:",
                 font=("Courier", 10, "bold"),
                 bg=self.PANEL_BG, fg=self.TEXT_CLR).pack(anchor="w")

        self.src_var = tk.StringVar(value="Delhi")
        src_menu = ttk.Combobox(panel, textvariable=self.src_var,
                                values=sorted(CITY_POSITIONS.keys()),
                                state="readonly", font=("Courier", 10))
        src_menu.pack(fill=tk.X, pady=(4, 12))

        # ── Destination dropdown ──
        tk.Label(panel, text="TO city:",
                 font=("Courier", 10, "bold"),
                 bg=self.PANEL_BG, fg=self.TEXT_CLR).pack(anchor="w")

        self.dst_var = tk.StringVar(value="Chennai")
        dst_menu = ttk.Combobox(panel, textvariable=self.dst_var,
                                values=sorted(CITY_POSITIONS.keys()),
                                state="readonly", font=("Courier", 10))
        dst_menu.pack(fill=tk.X, pady=(4, 20))

        # ── Find Route button ──
        tk.Button(panel, text="▶  Find Shortest Route",
                  font=("Courier", 10, "bold"),
                  bg=self.BTN_BG, fg=self.BTN_FG,
                  activebackground="#2563eb", activeforeground="#fff",
                  relief=tk.FLAT, padx=8, pady=8, cursor="hand2",
                  command=self._find_route).pack(fill=tk.X, pady=(0, 8))

        # ── Reset button ──
        tk.Button(panel, text="↺  Reset Map",
                  font=("Courier", 10),
                  bg="#374151", fg=self.TEXT_CLR,
                  activebackground="#4b5563",
                  relief=tk.FLAT, padx=8, pady=6, cursor="hand2",
                  command=self._reset).pack(fill=tk.X, pady=(0, 20))

        # ── Divider ──
        tk.Frame(panel, bg="#2e3a50", height=1).pack(fill=tk.X, pady=(0, 16))

        # ── Result box ──
        tk.Label(panel, text="RESULT", font=("Courier", 9, "bold"),
                 bg=self.PANEL_BG, fg="#64748b").pack(anchor="w")

        self.result_box = tk.Text(panel, height=10,
                                  font=("Courier", 9),
                                  bg=self.RESULT_BG, fg=self.TEXT_CLR,
                                  relief=tk.FLAT, wrap=tk.WORD,
                                  state=tk.DISABLED, padx=8, pady=8)
        self.result_box.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        # ── Legend ──
        tk.Frame(panel, bg="#2e3a50", height=1).pack(fill=tk.X, pady=12)
        self._legend(panel, self.START_CLR, "Source city")
        self._legend(panel, self.END_CLR,   "Destination city")
        self._legend(panel, self.PATH_CLR,  "Shortest path")
        self._legend(panel, self.ROAD_CLR,  "Regular road")

        # ── Canvas (map) ──
        self.canvas = tk.Canvas(self,
                                width=750, height=720,
                                bg=self.CANVAS_BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=12, pady=12)

    def _legend(self, parent, colour, label):
        row = tk.Frame(parent, bg=self.PANEL_BG)
        row.pack(anchor="w", pady=1)
        tk.Canvas(row, width=14, height=14, bg=colour,
                  highlightthickness=0).pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(row, text=label, font=("Courier", 8),
                 bg=self.PANEL_BG, fg="#94a3b8").pack(side=tk.LEFT)

    # ── Drawing helpers ────────────────────────

    def _draw_map(self, path=None):
        """Redraw the entire map. Highlight 'path' if provided."""
        self.canvas.delete("all")

        path_edges = set()
        if path:
            for i in range(len(path) - 1):
                path_edges.add((path[i], path[i + 1]))
                path_edges.add((path[i + 1], path[i]))

        # ── Draw roads ──
        for city_a, city_b, dist in ROADS:
            x1, y1 = CITY_POSITIONS[city_a]
            x2, y2 = CITY_POSITIONS[city_b]

            is_path_edge = (city_a, city_b) in path_edges

            colour = self.HIGHLIGHT if is_path_edge else self.ROAD_CLR
            width  = 4 if is_path_edge else 2
            dash   = () if is_path_edge else (5, 3)

            self.canvas.create_line(x1, y1, x2, y2,
                                    fill=colour, width=width, dash=dash)

            # Distance label on road
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            label_colour = "#f59e0b" if is_path_edge else "#475569"
            self.canvas.create_text(mx, my, text=f"{dist}km",
                                    font=("Courier", 7),
                                    fill=label_colour)

        # ── Draw cities ──
        src = self.src_var.get()
        dst = self.dst_var.get()

        for city, (x, y) in CITY_POSITIONS.items():
            r = self.CITY_RADIUS

            if city == src:
                colour = self.START_CLR
            elif city == dst:
                colour = self.END_CLR
            elif path and city in path:
                colour = self.PATH_CLR
            else:
                colour = self.CITY_CLR

            # Glow ring for path cities
            if path and city in path:
                self.canvas.create_oval(x - r - 5, y - r - 5,
                                        x + r + 5, y + r + 5,
                                        outline=colour, width=2,
                                        fill="")

            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill=colour, outline="#0f1117", width=2)

            # City name label
            self.canvas.create_text(x, y + r + 10, text=city,
                                    font=("Courier", 9, "bold"),
                                    fill=self.TEXT_CLR)

    # ── Core action ────────────────────────────

    def _find_route(self):
        src = self.src_var.get()
        dst = self.dst_var.get()

        if src == dst:
            messagebox.showwarning("Same City",
                                   "Please choose different source and destination cities.")
            return

        # Run Dijkstra's algorithm
        distance, path = dijkstra(self.graph, src, dst)

        if not path:
            self._show_result(f"No route found\nbetween {src} and {dst}.")
            self._draw_map()
            return

        # Build a step-by-step description
        steps = []
        total = 0
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            seg_dist = next(d for (c1, c2, d) in ROADS
                            if (c1 == a and c2 == b) or (c1 == b and c2 == a))
            total += seg_dist
            steps.append(f"  {a} → {b}  ({seg_dist} km)")

        result_text = (
            f"✅ Route found!\n\n"
            f"FROM : {src}\n"
            f"TO   : {dst}\n\n"
            f"PATH ({len(path) - 1} stops):\n"
            + "\n".join(steps) +
            f"\n\n{'─'*26}\n"
            f"TOTAL DISTANCE: {distance} km"
        )

        self._show_result(result_text)
        self._draw_map(path=path)

    def _reset(self):
        self._show_result("")
        self._draw_map()

    def _show_result(self, text):
        self.result_box.configure(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, text)
        self.result_box.configure(state=tk.DISABLED)


# ─────────────────────────────────────────────
#  5.  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = CityRouteFinder()
    app.mainloop()
