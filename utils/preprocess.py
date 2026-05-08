from typing import * 

CATEGORY_TO_FOL_MAP = {
    "AI_Lab_Support": ("UsesLab", "Lab1"),
    "Viva":           ("Eligible", "AI"),
    "Access":         ("UsesLab", "Lab1"),
    "Maintenance":    ("Eligible", "AI"),
}

def _build_booking_query(role: str, name: str, category: str) -> Optional[str]:
    '''
    Auto-build a FOL query from role, name, and category for booking eligibility check.
    Args:
        role (str): User role.
        name (str): User name.
        category (str): Requested service category.
    Returns:
        str | None: A FOL query string, or None if no mapping exists.
    '''
    mapping = CATEGORY_TO_FOL_MAP.get(category)
    if mapping is None:
        return None

    predicate, argument = mapping

    if role == "Instructor":
        return f"Instructor({name}, AI)"

    return f"{predicate}({name}, {argument})"


def preprocess_request(user_input: Dict[str, Any], request_id: str) -> Dict[str, Any]:
    '''
    Preprocess the user input to extract necessary information for routing.
    Args:
        user_input (Dict[str, Any]): The raw user input containing request details.
        request_id (str): The unique ID for the request.
    Returns:
        Dict[str, Any]: A dictionary containing preprocessed information for routing.
    '''

    if user_input["request_type"] == "Navigation_Only":
        return {
            "request_id": request_id,
            "name": user_input["name"],
            "role": user_input["role"],
            "request_type": user_input["request_type"],
            "current_location": user_input["current_location"],
            "destination": user_input["destination"],
            "needs_ann": False,
            "needs_logic": False,
            "needs_csp": False,
            "needs_search": True
        }
    
    elif user_input["request_type"] == "Eligibility_Check":
        return {
            "request_id": request_id,
            "name": user_input["name"],
            "role": user_input["role"],
            "request_type": user_input["request_type"],
            "query": user_input["query"],
            "needs_ann": False,
            "needs_logic": True,
            "needs_csp": False,
            "needs_search": False
         }
    elif user_input["request_type"] == "Booking_or_Scheduling":
        query = _build_booking_query(
            user_input["role"],
            user_input["name"],
            user_input["category"]
        )
        return {
            "request_id":       request_id,
            "name":             user_input["name"],
            "role":             user_input["role"],
            "request_type":     user_input["request_type"],
            "category":         user_input["category"],
            "preferred_slot":   user_input["preferred_slot"],
            "group_id":         user_input["group_id"],
            "current_location": user_input["current_location"],
            "query":            query,
            "needs_ann":        False,
            "needs_logic":      True,
            "needs_csp":        True,
            "needs_search":     user_input["current_location"] is not None
        }