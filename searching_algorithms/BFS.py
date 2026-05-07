from typing import Dict, List, Tuple

def bfs(graph: Dict[str, List[str]], start: str, goal: str) -> Tuple[List[str] | None, int]: 
    '''
    Perform Breadth-First Search on a graph to find the shortest path from start to goal.
    
    Args:
        graph (Dict[str, List[str]]): The graph represented as an adjacency list.
        start (str): The starting node.
        goal (str): The target node.
    
    Returns:
        Tuple[List[str] | None, int]: A tuple containing the path from start to goal and the number of steps taken.
    '''
    visited = set() 
    steps = 0
    queue = [(start, [start])]  # (current_node, path_to_current_node)

    while queue: 
        current_node, path = queue.pop(0) 
        steps += 1

        if current_node == goal: 
            return path, steps
        if current_node not in visited: 
            visited.add(current_node) 
            for neighbor in graph[current_node]: 
                if neighbor not in visited: 
                    queue.append((neighbor, path + [neighbor]))
    return None, steps