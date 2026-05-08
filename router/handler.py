from utils.graph_data import * 
from typing import * 
from utils.helper import get_validated_input, print_dict
from searching_algorithms import A_STAR, BFS, UCS
from utils.graph_data import campus_unweighted_graph, campus_weighted_graph, heuristics
from logic_kb import logic_engine
from csp.csp_solver import csp_assign

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


def eligibility_check(processed_output: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Handle eligibility check requests by querying the logic knowledge base.
    
    Args:
        processed_output (Dict[str, Any]): The preprocessed request output containing user role and query information.
    
    Returns:
        Dict[str, Any]: A dictionary containing the eligibility result and relevant details.
    '''
    query = processed_output.get("query")

    if query is None: 
        return {
            "query": None,
            "entailed": False,
            "explanation": "No valid query provided in the request."
        }

    result = logic_engine.ask_query(query)

    print_dict(processed_output, "Preprocessed Output")

    print_dict({
        "request_id": processed_output.get("request_id"),
        "selected_pipeline": select_pipeline(processed_output.get("request_type"))
    }, "Router Output")

    return result 
    

def booking_or_scheduling(processed_output: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Handle booking or scheduling requests using Logic KB eligibility check,
    CSP slot assignment, and optional Search for route guidance.
    Args:
        processed_output (Dict[str, Any]): The preprocessed request output.
    Returns:
        Dict[str, Any]: A dictionary containing eligibility, assignment, and optional route.
    '''
    query            = processed_output.get("query")
    category         = processed_output.get("category", "")
    preferred_slot   = processed_output.get("preferred_slot", 1)
    group_id         = processed_output.get("group_id")
    current_location = processed_output.get("current_location")

    print_dict(processed_output, "Preprocessed Output")
    print_dict({
        "request_id":        processed_output.get("request_id"),
        "selected_pipeline": select_pipeline(processed_output.get("request_type"))
    }, "Router Output")

    # --- Logic KB Step ---
    eligibility_output = {"allowed": True, "explanation": "No logic query provided; access assumed allowed."}

    if query:
        logic_result = logic_engine.ask_query(query)
        eligibility_output = {
            "allowed":     logic_result["entailed"],
            "explanation": logic_result["explanation"]
        }
        print_dict(eligibility_output, "Logic KB Output")

        if not eligibility_output["allowed"]:
            return {
                "eligibility": eligibility_output,
                "assignment":  None,
                "route":       None,
                "decision":    "rejected"
            }

    # --- CSP Step ---
    csp_result = csp_assign(category, preferred_slot, group_id)
    print_dict(csp_result, "CSP Output")

    if csp_result["decision"] == "rejected":
        return {
            "eligibility": eligibility_output,
            "assignment":  csp_result,
            "route":       None,
            "decision":    "rejected"
        }

    # --- Optional Search Step ---
    route_output = None
    destination  = csp_result.get("destination")

    if current_location and destination and current_location != destination:
        graph_type_map = {
            "1": "Unweighted Graph",
            "2": "Weighted Graph with Heuristic",
            "3": "Weighted Graph without Heuristic"
        }
        graph_type = get_validated_input(
            "Select Graph Type for Route (1-3): ",
            list(graph_type_map.values()),
            "Graph Types"
        )
        if graph_type == "Unweighted Graph":
            path, steps = BFS.bfs(campus_unweighted_graph, current_location, destination)
            route_output = {"algorithm_used": "BFS", "path": path, "steps": steps}
        elif graph_type == "Weighted Graph with Heuristic":
            path, cost, steps = A_STAR.a_star(campus_weighted_graph, heuristics, current_location, destination)
            route_output = {"algorithm_used": "A* Search", "path": path, "cost": cost, "steps": steps}
        else:
            path, cost, steps = UCS.ucs(campus_weighted_graph, current_location, destination)
            route_output = {"algorithm_used": "Uniform Cost Search", "path": path, "cost": cost, "steps": steps}

        print_dict(route_output, "Search Output")

    return {
        "eligibility": eligibility_output,
        "assignment":  csp_result,
        "route":       route_output,
        "decision":    "accepted"
    }