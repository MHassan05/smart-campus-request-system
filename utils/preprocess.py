
'''
IF request_type == "Navigation_Only":
pipeline = [Search]
ELIF request_type == "Eligibility_Check":
pipeline = [Logic_KB]
ELIF request_type == "Booking_or_Scheduling":
pipeline = [Logic_KB, CSP, optional Search]
ELIF request_type == "Urgent_Service_Request":
pipeline = [ANN, Logic_KB, CSP, optional Search]
ELIF request_type == "Full_Service_Request":
pipeline = [ANN, Logic_KB, CSP, Search]
ELSE:
reject request
7.2 Router output example
{
"request_id": "REQ205",
"selected_pipeline": ["ANN", "Logic_KB", "CSP", "Search"],
"needs_ann": true,
"needs_logic": true,
"needs_csp": true,
"needs_search": true
}

'''
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
            "request_type": user_input["request_type"],
            "current_location": user_input["current_location"],
            "destination": user_input["destination"],
            "needs_ann": False,
            "needs_logic": False,
            "needs_csp": False,
            "needs_search": True
        }
