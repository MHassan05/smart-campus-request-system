from utils.graph_data import * 
from typing import * 
from utils.helper import get_validated_input, print_dict
from searching_algorithms import A_STAR, BFS, UCS
from utils.graph_data import campus_unweighted_graph, campus_weighted_graph, heuristics


def select_pipeline(request_type: str) -> List[str]:
    '''
    Select the appropriate processing pipeline based on the request type.
    Args:
        request_type (str): The type of user request.
    Returns:
        List[str]: A list of components in the selected processing pipeline.
    '''
    if request_type == "Navigation_Only":
        return ["Search"]
    elif request_type == "Eligibility_Check":
        return ["Logic_KB"]
    elif request_type == "Booking_or_Scheduling":
        return ["Logic_KB", "CSP", "optional Search"]
    elif request_type == "Urgent_Service_Request":
        return ["ANN", "Logic_KB", "CSP", "optional Search"]
    elif request_type == "Full_Service_Request":
        return ["ANN", "Logic_KB", "CSP", "Search"]
    else:
        raise ValueError("Invalid request type. Request rejected.")
    

def navigate_only(processed_output: Dict[str, Any]) -> Dict[str, Any]: 
    '''
    Handle navigation-only requests by calculating the optimal route from the current location to the destination.
    
    Args:
        processed_output (Dict[str, Any]): The preprocessed request output containing location information.
    
    Returns:
        Dict[str, Any]: A dictionary containing the optimal route and estimated travel time.
    '''
    
    # first get which graph type to use
    graph_type_map = {
        "1": "Unweighted Graph ",
        "2": "Weighted Graph with Heuristic",
        "3": "Weighted Graph without Heuristic"
    }

    graph_type = get_validated_input(
        "Select Graph Type (1-3): ",
        list(graph_type_map.values()),
        "Graph Types"
    )

    print_dict(processed_output, "Preprocessed Output")
    
    print_dict({
        "request_id": processed_output.get("request_id"),
        "selected_pipeline": select_pipeline(processed_output.get("request_type"))
    }, "Router Output")

    # then get the optimal route and estimated travel time based on the selected graph type
    if graph_type == "Unweighted Graph": 
        path, steps = BFS.bfs(campus_unweighted_graph, processed_output["current_location"], processed_output["destination"])
        return {
            "algorithm_used": "BFS",
            "path": path, 
            "steps": steps
        }
        
    elif graph_type == "Weighted Graph with Heuristic":
        path, cost, steps = A_STAR.a_star(campus_weighted_graph, heuristics, processed_output["current_location"], processed_output["destination"])
        return {
            "algorithm_used": "A* Search",
            "path": path, 
            "cost": cost,
            "steps": steps
        }
    else:
        path, cost, steps = UCS.ucs(campus_weighted_graph, processed_output["current_location"], processed_output["destination"])
        return {
            "algorithm_used": "Uniform Cost Search",
            "path": path,
            "cost": cost,
            "steps": steps
        }
