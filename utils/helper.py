from typing import *

#================================================================
# Following code are used as helper functions for input validation and processing. 
#================================================================

def print_list(title: str, items: List[str]) -> None:
    '''
    Print a list of items with a title.
    Args:
        title (str): The title to display before the list.
        items (list): A list of items to print.
    '''
    print(f"\n{title}:")
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")
     

def get_validated_input(prompt: str, valid_options: List[str], title: str | None) -> str: 
    '''
    Prompt user for input and validate it against a list of valid options.
    Args:
        prompt (str): The message to display to the user.
        valid_options (list): A list of valid input options.
        title (str): The title to display before the list of options.
    Returns:
        str: The validated user input.
    '''

    if title:
        print_list(title, valid_options)

    while True:
        user_input = input(prompt).strip()
        if user_input.isdigit() and int(user_input) in list(range(1, len(valid_options) + 1)):
            return valid_options[int(user_input) - 1]
        print("Invalid input. Please select among the given options only.")
           

def get_int_in_range(prompt: str, min_value: int, max_value: int) -> int:
    '''
    Prompt user for an integer input and validate that it falls within a specified range.
    Args:
        prompt (str): The message to display to the user.
        min_value (int): The minimum valid value (inclusive).
        max_value (int): The maximum valid value (inclusive).
    Returns:
        int: The validated integer input from the user.
    '''
    while True:
        value = input(prompt).strip()
        if value.isdigit() and min_value <= int(value) <= max_value:
            return int(value)
        print(f"Invalid input. Enter a number between {min_value} and {max_value}.")


def get_name() -> str:
    '''
    Get and validate user's name, 
    it should be non-empty and only contain letters and spaces. 
    Returns:
        str: Validated name input from user.
    '''
    
    name = input("Enter Name: ").strip()

    while not name or not name.replace(" ", "").isalpha():
        print("Name cannot be empty or contain numbers/special characters.")
        name = input("Enter Name: ").strip()
    return name.title()


def get_role(valid_roles: List[str]) -> str:
    '''
    Get and validate user's role.
    Args:
        valid_roles (List[str]): A list of valid roles.
    Returns:
        str: The validated user role.
    '''

    return get_validated_input(
        "Enter Role (1-3): ",
        valid_roles,
        "Valid Roles"
    )


def get_request_type(request_type_map: Dict[str, str]) -> str:
    '''
    Get input from user for request type, and validate it between 1-5.
    Then return corresponding request type string based on the provided mapping.
    Args:
        request_type_map (Dict[str, str]): A dictionary mapping request type choices to their descriptions.
    Returns:
        str: The validated user request type.
    '''

    return get_validated_input(
        "Enter Request Type (1-5): ",
        list(request_type_map.values()),
        "Request Types"
    ) 


def get_menu_choice(valid_choices: list[str]) -> str:
    '''
    Get validated menu choice from user.
    Args: 
        valid_choices (list[str]): A list of valid choices to select from.
    Returns: 
        str: Validated user input in str format. 
    '''

    while True:

        choice = input("Enter choice: ").strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Try again.")


def get_non_empty_input(field_name: str) -> str:
    '''
    Get non-empty input from user.
    Args: 
        field_name (str): The name of the field for which input is being requested. 
    Returns: 
        str: User input in str format. 
    '''

    while True:

        value = input(f"Enter {field_name}: ").strip()

        if value:
            return value

        print(f"{field_name} cannot be empty.")


def print_dict(data: Dict[str, Any], title: str)-> None: 
    '''
    Print a dictionary in a readable format.
    Args:
        data (Dict[str, Any]): The dictionary to print.
        title (str): The title for the dictionary.
    '''
    print() 
    print(f"{title}:")
    for key, value in data.items():
        print(f"{key}: {value}")
    print() 

# ===============================================================================
# Code below this is for handling possible fields based on different request types, 
# I put them separately to make the main get_user_input function cleaner and more modular.
# ===============================================================================

def get_navigation_inputs(valid_locations: List[str]) -> Tuple[str, str]:
    '''
    Prompt user to enter current and destination locations for navigation requests, 
    and validate them against the list of valid_locations.
    Args:
    valid_locations (List[str]): A list of valid locations to choose from.
    Returns:
    Tuple[str, str]: A tuple containing the validated current location and destination.
    '''
    current_location = get_validated_input(
            "Enter Current Location (1-{}): ".format(len(valid_locations)),
            valid_locations,
            None 
        )
    while True: 
        destination = get_validated_input(
            "Enter Destination (1-{}): ".format(len(valid_locations)),
            valid_locations,
            None
        )
        if destination != current_location:
            break
        print("Destination cannot be the same as current location.")

    return current_location, destination


def get_eligibility_inputs(role: str, name: str) -> str | None:
    '''
    Get and validate user's query for eligibility checks.
    Args:
        role (str): The user's role.
        name (str): The user's name.
    Returns:
        str | None: The validated FOL query string, or None if invalid.
    '''
    if role == "Student":
        print("\nEligibility Options:")
        print("1. Check AI Course Eligibility")   
        print("2. Check Lab Access")              
        choice = get_menu_choice(["1", "2"])

        if choice == "1":
            course = get_non_empty_input("Course Name (e.g. AI)")
            return f"Eligible({name}, {course})"

        elif choice == "2":
            lab = get_non_empty_input("Lab Name (e.g. Lab1)")
            return f"UsesLab({name}, {lab})"

    elif role == "Instructor":
        print("\nEligibility Options:")
        print("1. Check Instructor Status")        
        print("2. Check Lab Access")               
        choice = get_menu_choice(["1", "2"])

        if choice == "1":
            course = get_non_empty_input("Course Name (e.g. AI)")
            return f"Instructor({name}, {course})"  
        elif choice == "2":
            lab = get_non_empty_input("Lab Name (e.g. Lab1)")
            return f"UsesLab({name}, {lab})"

    else:
        # Staff or unknown roles have no rules in this KB
        print(f"Role '{role}' has no eligibility rules defined in the current Knowledge Base.")
        return None
    

def get_booking_inputs(valid_categories: List[str]) -> Tuple[str, int, str | None]:
    '''
    Get and validate user's input for booking or scheduling requests, including category, preferred slot, and optional group ID. 
    Args:
        valid_categories (List[str]): A list of valid categories to choose from.
    Returns:
        Tuple[str, int, str | None]: A tuple containing the validated category, preferred slot, and optional group ID.
    '''
    category = get_validated_input(
        "Enter Category (1-{}): ".format(len(valid_categories)),
        valid_categories,
        None 
    )
    preferred_slot = get_int_in_range("Enter Preferred Slot (1-4): ", 1, 4)
    group_id = input("Enter Group ID (optional): ").strip() or None

    return category, preferred_slot, group_id


def get_yes_no(prompt: str) -> str:
    '''
    Get and validate user's yes/no response.
    Args:
        prompt (str): The message to display to the user.
    Returns:
        str: The validated user response ('yes' or 'no').
    '''
    while True:
        val = input(prompt).strip().lower()
        if val in ["yes", "no", "y", "n"]:
            return val
        print("Invalid input. Enter 'yes/y' or 'no/n'.")


def get_urgent_service_inputs(valid_categories: List[str], valid_locations: List[str]) -> Tuple[str, str, int, int, int, int]:
    '''
    Get and validate user's input for urgent service requests, including category, current location, severity, time sensitivity, crowd level, and preferred slot.
    Args:
        valid_categories (List[str]): A list of valid categories to choose from.
        valid_locations (List[str]): A list of valid locations to choose from.
    Returns:
        Tuple[str, str, int, int, int, int]: A tuple containing the validated category, current location, severity level, time sensitivity level, crowd level, and preferred slot.
    '''
    category = get_validated_input(
        "Enter Category (1-{}): ".format(len(valid_categories)),
        valid_categories,
        "Available Categories" 
    )
    current_location = get_validated_input(
        "Enter Current Location (1-{}): ".format(len(valid_locations)),
        valid_locations,
        "Available Locations"
    )
    severity = get_int_in_range("Enter Severity (1-10): ", 1, 10)
    time_sensitivity = get_int_in_range("Enter Time Sensitivity (1-10): ", 1, 10)
    crowd_level = get_int_in_range("Enter Crowd Level (1-10): ", 1, 10)
    preferred_slot = get_int_in_range("Enter Preferred Slot (1-4): ", 1, 4)

    return category, current_location, severity, time_sensitivity, crowd_level, preferred_slot


def get_full_service_inputs(valid_categories: List[str], valid_locations: List[str]) -> Tuple[str, str, int, int, int, int, str | None]:
    '''
    Get and validate user's input for full service requests, including category, current location, preferred slot, severity, time sensitivity, crowd level, and optional description note.
    Args:
        valid_categories (List[str]): A list of valid categories to choose from.
        valid_locations (List[str]): A list of valid locations to choose from.
    Returns:
        Tuple[str, str, int, int, int, int, str | None]: A tuple containing the validated category, current location, preferred slot, severity level, time sensitivity level, crowd level, and optional description note.
    '''
    category = get_validated_input(
        "Enter Category (1-{}): ".format(len(valid_categories)),
        valid_categories,
        "Available Categories"
    )
    current_location = get_validated_input(
        "Enter Current Location (1-{}): ".format(len(valid_locations)),
        valid_locations,
        "Available Locations"
    )
    preferred_slot = get_int_in_range("Enter Preferred Slot (1-4): ", 1, 4)
    severity = get_int_in_range("Enter Severity (1-10): ", 1, 10)
    time_sensitivity = get_int_in_range("Enter Time Sensitivity (1-10): ", 1, 10)
    crowd_level = get_int_in_range("Enter Crowd Level (1-10): ", 1, 10)
    description_note = input("Enter Description Note (optional): ").strip() or None

    return category, current_location, preferred_slot, severity, time_sensitivity, crowd_level, description_note
