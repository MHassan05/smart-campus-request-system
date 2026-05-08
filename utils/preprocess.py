from typing import * 

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
    