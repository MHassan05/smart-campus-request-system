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

def get_navigation_inputs() -> Tuple[str, str]: 
    '''
    Get and validate user's current location and destination for navigation requests.
    Returns:
        Tuple[str, str]: A tuple containing the validated current location and destination.
    '''
    curr = get_location("Enter Current Location: ", VALID_LOCATIONS)
    dest = get_location("Enter Destination: ", VALID_LOCATIONS)
    while dest == curr:
             print("Destination cannot be same as current location.")
             dest = get_location("Enter Destination: ", VALID_LOCATIONS)
    return curr, dest


def get_eligibility_inputs() -> str:
    '''
    Get and validate user's query for eligibility checks.
    Returns:
        str: The validated user query.
    '''

    while True:
        query = input("Enter Query (e.g. UsesLab(DrKhan, Lab1)): ").strip()
        if validate_query(query):
            return query
        print("Invalid query format.")

def get_booking_inputs() -> Tuple[str, str, str | None]:
    '''
    Get and validate user's category and preferred slot for booking requests.
    Returns:
        Tuple[str, str, str | None]: A tuple containing the validated category, preferred slot, and group ID.
    '''

    return get_category(VALID_CATEGORIES), get_preferred_slot(), get_group_id()


def get_urgent_service_inputs() -> Tuple[str, str, str, str, str, str | None]:
    '''
    Get and validate user's inputs for urgent service requests.
    Returns:
        Tuple[str, str, str, str, str, str | None]: A tuple containing the validated category, current location, severity, time sensitivity, crowd level, and preferred slot(Optional).
    '''

    category = get_category(VALID_CATEGORIES)
    print_list("Available Locations", VALID_LOCATIONS)
    current_location = get_location("Enter Current Location: ", VALID_LOCATIONS)

    severity = get_severity()
    time_sensitivity = get_time_sensitivity()
    crowd_level = get_crowd_level()
    preferred_slot = get_preferred_slot(allow_skip=True)

    return category, current_location, severity, time_sensitivity, crowd_level, preferred_slot


def get_full_service_inputs():
    category = get_category(VALID_CATEGORIES)
    print_list("Available Locations", VALID_LOCATIONS)
    current_location = get_location("Enter Current Location: ", VALID_LOCATIONS)

    preferred_slot = get_preferred_slot()
    severity = get_severity()
    time_sensitivity = get_time_sensitivity()
    crowd_level = get_crowd_level()
    description_note = get_description()

    return (
        category, current_location, preferred_slot, severity, 
        time_sensitivity, crowd_level, description_note
    )



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
        current_location, destination = get_navigation_inputs()
         
    elif request_type == "Eligibility_Check":
        query = get_eligibility_inputs() 

    elif request_type == "Booking_or_Scheduling":
        print_list("Available Categories", VALID_CATEGORIES)
        category, preferred_slot, group_id = get_booking_inputs()

        if get_yes_no("Do you need route guidance? (yes/no): ") == "yes":
            print_list("Available Locations", VALID_LOCATIONS)
            current_location = get_location("Enter Current Location: ", VALID_LOCATIONS)

    elif request_type == "Urgent_Service_Request":
        (category, current_location, 
        severity, time_sensitivity, 
        crowd_level, preferred_slot) = get_urgent_service_inputs()

    elif request_type == "Full_Service_Request":
        (category, current_location, preferred_slot, severity, 
         time_sensitivity, crowd_level, description_note) = get_full_service_inputs()

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
