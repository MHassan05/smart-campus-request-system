from utils.graph_data import * 
from typing import * 
from utils.helper import get_validated_input, print_dict
from searching_algorithms import A_STAR, BFS, UCS
from utils.graph_data import campus_unweighted_graph, campus_weighted_graph, heuristics
from logic_kb import logic_engine
from csp.csp_solver import csp_assign
from ann.ann_engine import run_ann

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

    if query == "REJECTED":
        return {
            "eligibility": {
                "allowed":     False,
                "explanation": f"Role '{processed_output.get('role')}' is not permitted to book '{category}'."
            },
            "assignment": None,
            "route":      None,
            "decision":   "rejected"
        }

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


def urgent_service_request(processed_output: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Handle urgent service requests using ANN → Logic → CSP → optional Search pipeline.
    Args:
        processed_output (Dict[str, Any]): The preprocessed request output.
    Returns:
        Dict[str, Any]: Combined ANN, eligibility, CSP, and optional route results.
    '''
    print_dict(processed_output, "Preprocessed Output")

    print_dict({
        "request_id":       processed_output.get("request_id"),
        "selected_pipeline": select_pipeline(processed_output.get("request_type"))
    }, "Router Output")

    # ANN
    ann_result = run_ann(processed_output, distance=4, eligibility=True)

    # Logic KB check
    query = processed_output.get("query")
    if query == "REJECTED":
        return {
            "ann":         None,
            "eligibility": {
                "allowed":     False,
                "explanation": f"Role '{processed_output.get('role')}' is not permitted to book '{processed_output.get('category')}'."
            },
            "csp":   None,
            "route": None
        }
    
    if query:
        logic_result = logic_engine.ask_query(query)
        eligibility_result = {
            "allowed":     logic_result["entailed"],
            "explanation": logic_result["explanation"]
        }
    else:
        eligibility_result = {
            "allowed":     True,
            "explanation": "No logic query provided; access assumed allowed."
        }

    if not eligibility_result["allowed"]:
        return {
            "ann":         ann_result,
            "eligibility": eligibility_result,
            "csp":         None,
            "route":       None
        }

    # CSP
    csp_result = csp_assign(
        processed_output.get("category"),
        processed_output.get("preferred_slot"),
        processed_output.get("group_id")
    )

    # Search
    route_result = None
    if csp_result["decision"] == "accepted":
        current_location = processed_output.get("current_location")
        destination      = csp_result.get("destination")

        if current_location and destination and current_location != destination:
            graph_type = get_validated_input(
                "Select Graph Type for Route (1-3): ",
                ["Unweighted Graph", "Weighted Graph with Heuristic", "Weighted Graph without Heuristic"],
                "Graph Types"
            )
            if graph_type == "Unweighted Graph":
                path, _ = BFS.bfs(campus_unweighted_graph, current_location, destination)
                route_result = {
                    "algorithm_used": "BFS",
                    "path":           path,
                    "steps":          len(path) - 1
                }
            elif graph_type == "Weighted Graph with Heuristic":
                path, cost, _ = A_STAR.a_star(campus_weighted_graph, heuristics, current_location, destination)
                route_result = {
                    "algorithm_used": "A* Search",
                    "path":           path,
                    "cost":           cost,
                    "steps":          len(path) - 1
                }
            else:
                path, cost, _ = UCS.ucs(campus_weighted_graph, current_location, destination)
                route_result = {
                    "algorithm_used": "Uniform Cost Search",
                    "path":           path,
                    "cost":           cost,
                    "steps":          len(path) - 1
                }
            print_dict(route_result, "Search Output")

    return {
        "ann":         ann_result,
        "eligibility": eligibility_result,
        "csp":         csp_result,
        "route":       route_result
    }


def full_service_request(processed_output: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Handle full service requests using ANN → Logic → CSP → Search pipeline.
    Args:
        processed_output (Dict[str, Any]): The preprocessed request output.
    Returns:
        Dict[str, Any]: Combined ANN, eligibility, CSP, and route results.
    '''
    print_dict(processed_output, "Preprocessed Output")

    print_dict({
        "request_id":        processed_output.get("request_id"),
        "selected_pipeline": select_pipeline(processed_output.get("request_type"))
    }, "Router Output")

    # ANN
    ann_result = run_ann(processed_output, distance=4, eligibility=True)

    print_dict(ann_result, "ANN Output")

    # Logic KB check
    query = processed_output.get("query")
    if query == "REJECTED":
        return {
            "ann":         None,
            "eligibility": {
                "allowed":     False,
                "explanation": f"Role '{processed_output.get('role')}' is not permitted to book '{processed_output.get('category')}'."
            },
            "csp":   None,
            "route": None
        }
    if query:
        logic_result = logic_engine.ask_query(query)
        eligibility_result = {
            "allowed":     logic_result["entailed"],
            "explanation": logic_result["explanation"]
        }
    else:
        eligibility_result = {
            "allowed":     True,
            "explanation": "No logic query provided; access assumed allowed."
        }

    if not eligibility_result["allowed"]:
        return {
            "ann":         ann_result,
            "eligibility": eligibility_result,
            "csp":         None,
            "route":       None
        }
    
    print_dict(eligibility_result, "Logic / KB Output")

    # CSP
    csp_result = csp_assign(
        processed_output.get("category"),
        processed_output.get("preferred_slot"),
        processed_output.get("group_id")
    )

    print_dict(csp_result, "CSP Output")

    # Search — always runs for Full_Service_Request
    route_result = None
    if csp_result["decision"] == "accepted":
        path, cost, _ = A_STAR.a_star(campus_weighted_graph, heuristics, processed_output["current_location"], csp_result["destination"])
        route_result = {
            "algorithm_used": "A*",
            "path":           path,
            "cost":           cost,
            "steps":          len(path) - 1
        }

    return {
        "ann":         ann_result,
        "eligibility": eligibility_result,
        "csp":         csp_result,
        "route":       route_result
    }