import heapq
import time


# 1. Map of Mahikeng local municipality
# BUG FIX: The graph was incomplete - only Disaneng was defined.
# FIXED: All nodes and their neighbours added as an undirected graph.

graph = {
    "Disaneng":    ["Mahikeng", "Madibogo"],
    "Mahikeng":    ["Disaneng", "Mmabatho", "Slurry", "Bakerville", "Madibogo"],
    "Mmabatho":    ["Mahikeng", "Slurry"],
    "Slurry":      ["Mahikeng", "Mmabatho", "Zeerust", "Groot Marico", "Bakerville"],
    "Zeerust":     ["Slurry", "Groot Marico"],
    "Groot Marico":["Slurry", "Zeerust"],
    "Bakerville":  ["Mahikeng", "Slurry", "Lichtenburg"],
    "Lichtenburg": ["Bakerville", "Coligny"],
    "Coligny":     ["Lichtenburg", "Ottosdal"],
    "Ottosdal":    ["Coligny", "Sannieshof"],
    "Sannieshof":  ["Ottosdal", "Delareyville", "Madibogo"],
    "Delareyville":["Sannieshof"],
    "Madibogo":    ["Disaneng", "Mahikeng", "Sannieshof"],
}


# 2. Distance between areas (km)
# No changes needed — all edge weights are correct and present.

weights = {
    ("Disaneng", "Mahikeng"):       25,
    ("Disaneng", "Madibogo"):       35,
    ("Mahikeng", "Mmabatho"):       10,
    ("Mahikeng", "Slurry"):         20,
    ("Mahikeng", "Bakerville"):     35,
    ("Mahikeng", "Madibogo"):       30,
    ("Mmabatho", "Slurry"):         15,
    ("Slurry", "Zeerust"):          35,
    ("Slurry", "Groot Marico"):     40,
    ("Slurry", "Bakerville"):       25,
    ("Zeerust", "Groot Marico"):    20,
    ("Bakerville", "Lichtenburg"):  20,
    ("Lichtenburg", "Coligny"):     30,
    ("Coligny", "Ottosdal"):        35,
    ("Ottosdal", "Sannieshof"):     25,
    ("Sannieshof", "Delareyville"): 30,
    ("Madibogo", "Sannieshof"):     35,
}


# 3. Heuristic to goal = Coligny
# BUG FIX: The heuristic dictionary was completely empty.
# FIXED: Using the "Traffic per city" values from the PDF as heuristic estimates.
# The goal node (Coligny) must have heuristic = 0 (we are already there).
# These are admissible estimates — the higher the traffic/distance, the further from goal.

heuristic = {
    "Disaneng":     70,
    "Mahikeng":     50,
    "Mmabatho":     55,
    "Slurry":       45,
    "Zeerust":      65,
    "Groot Marico": 75,
    "Bakerville":   30,
    "Lichtenburg":  20,
    "Coligny":       0,   # Goal node — heuristic must be 0
    "Ottosdal":     25,
    "Sannieshof":   40,
    "Delareyville": 55,
    "Madibogo":     60,
}


# 4. Undirected edge cost lookup
# No changes needed — logic is correct.

def get_cost(a, b, weights):
    if (a, b) in weights:
        return weights[(a, b)]
    elif (b, a) in weights:
        return weights[(b, a)]
    else:
        raise ValueError(f"No weight found between '{a}' and '{b}'")


# 5. A* Search algorithm
# No changes needed — the core algorithm is correct.

def astar(graph, weights, heuristic, start, goal):
    open_set = []
    heapq.heappush(open_set, (heuristic[start], start))

    came_from = {}
    g_score = {node: float("inf") for node in graph}
    g_score[start] = 0

    f_score = {node: float("inf") for node in graph}
    f_score[start] = heuristic[start]

    visited_order = []

    while open_set:
        _, current = heapq.heappop(open_set)

        if current not in visited_order:
            visited_order.append(current)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, visited_order, g_score[goal]

        for neighbor in graph[current]:
            cost = get_cost(current, neighbor, weights)
            tentative_g = g_score[current] + cost

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, visited_order, float("inf")


# 6. Run the A* search
# BUG FIX 1: goal was set to " " (a blank space string) instead of "Coligny".
# FIXED: goal = "Coligny"

start = "Disaneng"
goal  = "Coligny"

path, visited_order, total_cost = astar(graph, weights, heuristic, start, goal)


# 7. Simulate and display the result
# BUG FIX 2 (from testcase file): The function was named simulate_path but
#   called as simulte_path (typo — missing 'a').
# BUG FIX 3: Variables pat, visit_order, tot_cost were used inside the function
#   but never defined — they must be the returned values from astar().
# FIXED: Renamed variables consistently and passed correct values.

def simulate_path(path):
    print("\n Truck traveling...\n")
    for node in path:
        print(f"  Truck is now at: {node}")
        time.sleep(0.5)
    print("\nDestination reached!")

    print("\nVisited Order:", visited_order)
    print("Optimal Path: ", path)
    print("Total Cost:   ", total_cost, "km")

simulate_path(path)
