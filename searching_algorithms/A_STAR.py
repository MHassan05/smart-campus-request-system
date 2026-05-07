from typing import Dict, Tuple, List
import heapq
import math


def heuristic_distance(
    node: str,
    goal: str,
    heuristics: Dict[str, Tuple[int, int]]
) -> float:

    x1, y1 = heuristics[node]
    x2, y2 = heuristics[goal]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def a_star(graph, heuristics, start, goal):

    # (f_cost, g_cost, current_node, path)
    open_set = []

    start_h = heuristic_distance(start, goal, heuristics)

    heapq.heappush(
        open_set,
        (start_h, 0, start, [start])
    )

    g_costs = {start: 0}

    visited = set()

    steps = 0

    while open_set:

        f_cost, current_g, current_node, path = heapq.heappop(open_set)

        steps += 1

        if current_node == goal:
            return path, current_g, steps

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, edge_cost in graph.get(current_node, {}).items():

            tentative_g = current_g + edge_cost

            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:

                g_costs[neighbor] = tentative_g

                h = heuristic_distance(
                    neighbor,
                    goal,
                    heuristics
                )

                f = tentative_g + h

                heapq.heappush(
                    open_set,
                    (f, tentative_g, neighbor, path + [neighbor])
                )

    return [], float("inf"), steps

if __name__ == "__main__":

    campus_weighted_graph = {

        "Main_Gate": {
            "Admin_Block": 4,
            "Parking": 2,
            "Bus_Stop": 1,
            "Hostel": 5
        },

        "Admin_Block": {
            "Main_Gate": 4,
            "Student_Services": 1,
            "Exam_Hall": 2
        },

        "Student_Services": {
            "Admin_Block": 1,
            "Library": 2
        },

        "Exam_Hall": {
            "Admin_Block": 2,
            "Seminar_Room": 1,
            "Science_Block": 3
        },

        "Seminar_Room": {
            "Exam_Hall": 1,
            "Science_Block": 2
        },

        "Parking": {
            "Main_Gate": 2,
            "Bus_Stop": 2,
            "Science_Block": 3
        },

        "Bus_Stop": {
            "Main_Gate": 1,
            "Parking": 2,
            "Medical_Center": 2
        },

        "Medical_Center": {
            "Bus_Stop": 2,
            "Hostel": 3
        },

        "Hostel": {
            "Main_Gate": 5,
            "Medical_Center": 3,
            "Cafeteria": 2
        },

        "Cafeteria": {
            "Hostel": 2,
            "Library": 2,
            "Science_Block": 3
        },

        "Library": {
            "Student_Services": 2,
            "Cafeteria": 2,
            "AI_Lab": 3
        },

        "Science_Block": {
            "Parking": 3,
            "Exam_Hall": 3,
            "Seminar_Room": 2,
            "Cafeteria": 3,
            "AI_Lab": 1
        },

        "AI_Lab": {
            "Library": 3,
            "Science_Block": 1
        }
    }

    heuristics = {

        "Main_Gate": (0, 4),
        "Admin_Block": (3, 5),
        "Student_Services": (6, 5),
        "Exam_Hall": (8, 5),
        "Seminar_Room": (10, 4),
        "Parking": (2, 4),
        "Bus_Stop": (0, 1),
        "Medical_Center": (1, 1),
        "Hostel": (2, 0),
        "Cafeteria": (4, 1),
        "Library": (6, 2),
        "Science_Block": (7, 1),
        "AI_Lab": (9, 2)
    }

    start = "Main_Gate"
    goal = "AI_Lab"

    path, cost, steps = a_star(
        campus_weighted_graph,
        heuristics,
        start,
        goal
    )

    print("\n===== A* SEARCH RESULT =====")
    print("Start Node :", start)
    print("Goal Node  :", goal)
    print("Path Found :", " -> ".join(path))
    print("Total Cost :", cost)
    print("Steps Taken:", steps)