from utils.graph_data import campus_unweighted_graph 
from utils.helper import * 

# Available roles, categories, locations, and request types  
VALID_ROLES = ["Student", "Instructor", "Staff"]
VALID_CATEGORIES = ["AI_Lab_Support", "Viva", "Access", "Maintenance"]
VALID_LOCATIONS = list(campus_unweighted_graph.keys())
REQUEST_TYPE_MAP = {
    "1": "Navigation_Only",
    "2": "Eligibility_Check",
    "3": "Booking_or_Scheduling",
    "4": "Urgent_Service_Request",
    "5": "Full_Service_Request"
}


def get_user_input(): 
    '''
    Get input form user then validate and normalize it. 
    Returns:
        dict: A dictionary containing the validated and normalized user input.
    '''

    # base fields 
    name = get_name() 
    role = get_role(VALID_ROLES)
    request_type = get_request_type(REQUEST_TYPE_MAP) 

    # Possible fields 
    category = None
    current_location = None
    destination = None
    preferred_slot = None
    severity = None
    time_sensitivity = None
    crowd_level = None
    group_id = None
    query = None
    description_note = None


    if request_type == "Navigation_Only": 
        print_list("Available Locations", VALID_LOCATIONS)
        current_location, destination = get_navigation_inputs(VALID_LOCATIONS)
         
    elif request_type == "Eligibility_Check":
        query = get_eligibility_inputs() 

    elif request_type == "Booking_or_Scheduling":
        print_list("Available Categories", VALID_CATEGORIES)
        category, preferred_slot, group_id = get_booking_inputs(VALID_CATEGORIES)

        if get_yes_no("Do you need route guidance? (yes/no): ") == "yes":
            print_list("Available Locations", VALID_LOCATIONS)
            current_location = get_validated_input("Enter Current Location: ", VALID_LOCATIONS, None)

    elif request_type == "Urgent_Service_Request":
        (category, current_location, 
        severity, time_sensitivity, 
        crowd_level, preferred_slot) = get_urgent_service_inputs(VALID_CATEGORIES, VALID_LOCATIONS)

    elif request_type == "Full_Service_Request":
        (category, current_location, preferred_slot, severity, 
         time_sensitivity, crowd_level, description_note) = get_full_service_inputs(VALID_CATEGORIES, VALID_LOCATIONS)

    return {
        "name": name,
        "role": role,
        "request_type": request_type,
        "category": category,
        "current_location": current_location,
        "destination": destination,
        "preferred_slot": preferred_slot,
        "severity": severity,
        "time_sensitivity": time_sensitivity,
        "crowd_level": crowd_level,
        "group_id": group_id,
        "query": query,
        "description_note": description_note
    }

if __name__ == "__main__":
    print(get_user_input())
