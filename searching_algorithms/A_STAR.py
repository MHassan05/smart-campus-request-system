from typing import Dict, Tuple, List
import heapq
import math

def a_star(graph: Dict[str, Dict[str, int]], heuristics: Dict[str, Tuple[int, int]], start: str, goal: str) -> Tuple[List[str], int, int]: 
    '''
    We will be using Euclidean distance as the heuristic for A* search. 
    Because the shortest path between two points is a straight line, the Euclidean distance 
    provides an admissible heuristic that never overestimates the true cost to reach the goal.
    Args:
        graph (Dict[str, Dict[str, int]]): The weighted graph representing the campus layout.
        heuristics (Dict[str, Tuple[int, int]]): A dictionary containing heuristic values for each node.
        start (str): The starting location.
        goal (str): The destination location.
    Returns:
        Tuple[List[str], int, int]: A tuple containing the optimal path, total cost, and number of steps taken.
    '''

    def euclidean(a, b):
        raw = math.sqrt((heuristics[a][0] - heuristics[b][0])**2 + (heuristics[a][1] - heuristics[b][1])**2)
        return raw * 0.5 # Multiplied by 0.5 to scale down the heuristic values for better performance

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    steps = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        steps += 1

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal], steps

        for neighbor, weight in graph[current].items():
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return [], -1, steps


if __name__ == "__main__":
    campus_weighted_graph = {
        "Main_Gate": {
            "Admin_Block": 4, "Parking": 2, "Bus_Stop": 1, "Hostel": 5
            },
        "Admin_Block": {
            "Main_Gate": 4, "Student_Services": 1, "Exam_Hall": 2
            },
        "Student_Services": {
            "Admin_Block": 1, "Library": 2
            },
        "Exam_Hall": {
            "Admin_Block": 2, "Seminar_Room": 1, "Science_Block": 3
            },
        "Seminar_Room": {
            "Exam_Hall": 1, "Science_Block": 2
            },
        "Parking": {
            "Main_Gate": 2, "Bus_Stop": 2, "Science_Block": 3
        },
        "Bus_Stop": {
            "Main_Gate": 1, "Parking": 2, "Medical_Center": 2
        },
        "Medical_Center": {
            "Bus_Stop": 2, "Hostel": 3
        },
        "Hostel": {
            "Main_Gate": 5, "Medical_Center": 3, "Cafeteria": 2
        },
        "Cafeteria": {
            "Hostel": 2, "Library": 2, "Science_Block": 3
        },
        "Library": {
            "Student_Services": 2, "Cafeteria": 2, "AI_Lab": 3
        },
        "Science_Block": {
            "Parking": 3, "Exam_Hall": 3, "Seminar_Room": 2, "Cafeteria": 3, "AI_Lab": 1
        },
        "AI_Lab": {
            "Library": 3, "Science_Block": 1
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

    test_cases = [
        ("Hostel", "AI_Lab"), 
        ("Main_Gate", "AI_Lab"),
        ("Bus_Stop", "Seminar_Room"),
        ("Hostel", "Exam_Hall"),
        ("Parking", "Library"),
    ]

    for start, goal in test_cases:
        path, cost, steps = a_star(campus_weighted_graph, heuristics, start, goal)
        print(f"Start: {start} -> Goal: {goal}")
        print(f"  Path  : {' -> '.join(path)}")
        print(f"  Cost  : {cost}")
        print(f"  Steps : {steps}")
        print()