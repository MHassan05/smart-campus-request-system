from typing import Dict, List, Tuple

def ucs(graph: Dict[str, List[Tuple[str, int]]], start: str, goal: str) -> Tuple[List[str], int, int]: 
    '''
    Perform Uniform Cost Search on a graph to find the least costly path from start to goal.
    
    Args:
        graph (Dict[str, List[Tuple[str, int]]]): The graph represented as an adjacency list with edge costs.
        start (str): The starting node.
        goal (str): The target node.
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing the path from start to goal, the total cost of that path, and the number of steps taken.
    '''
    visited = set() 
    steps = 0
    queue = [(0, start, [start])]  

    while queue: 
        cost, current_node, path = queue.pop(0) 
        steps += 1

        if current_node == goal: 
            return path, cost, steps
        if current_node not in visited: 
            visited.add(current_node) 
            for neighbor, cost in graph[current_node]: 
                if neighbor not in visited: 
                    queue.append((cost + cost, neighbor, path + [neighbor]))
                    queue.sort(key=lambda x: x[0])  
    return None, float('inf'), steps