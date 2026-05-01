from typing import *

def get_validated_input(prompt: str, valid_options: List[str]) -> str:
    '''
    Prompt user for input and validate it against a list of valid options.
    Args:
        prompt (str): The message to display to the user.
        valid_options (list): A list of valid input options.
    Returns:
        str: The validated user input.
    '''
    while True:
        user_input = normalize_input(input(prompt).strip().lower())
        # debug line 
        print(f"User input: {user_input}")
        for option in valid_options:
            if user_input.lower() == option.lower():
                return option
        print("Invalid input. Please try again.")



def print_list(title: str, items: List[str]) -> None:
    '''
    Print a list of items with a title.
    Args:
        title (str): The title to display before the list.
        items (list): A list of items to print.
    '''
    print(f"\n{title}:")
    for item in items:
        print(f"- {item}")



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
        "Enter Role (student / instructor / staff): ",
        valid_roles
    ).capitalize() 



def get_request_type(request_type_map: Dict[str, str]) -> str:
    '''
    Get and validate user's request type.
    Args:
        request_type_map (Dict[str, str]): A dictionary mapping request type choices to their descriptions.
    Returns:
        str: The validated user request type.
    '''

    print("\nEnter Request Type:")
    for key, value in request_type_map.items():
        print(f"{key}. {value}")

    while True:
        choice = normalize_input(input("Enter Choice (1-5): ").strip())
        if choice in request_type_map:
            request_type = request_type_map[choice]
            break
        print("Invalid choice. Enter a number between 1 and 5.")

    return request_type



def get_location(prompt: str, valid_locations: List[str]) -> str:
    '''
    Get and validate user's location (current or destination).
    Args:
        prompt (str): The message to display to the user.
        valid_locations (List[str]): A list of valid locations.
    Returns:
        str: The validated user location.
    '''
    return get_validated_input(prompt, valid_locations)



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



def validate_query(query: str) -> bool:
    '''
    Validate user's query for eligibility checks.
    Returns:
        bool: True if the query is valid, False otherwise.
    '''
    return "(" in query and ")" in query and len(query) > 3



def get_category(valid_categories: List[str]) -> str:
    '''
    Get and validate user's category for booking requests.
    Returns:
        str: The validated user category.
    '''
    print_list("Available Categories", valid_categories)
    return get_validated_input("Enter Category: ", valid_categories)



def get_preferred_slot(allow_skip: bool = False) -> str: 
    '''
    Get and validate user's preferred slot for booking requests.
    Args:
        allow_skip (bool): Whether to allow the user to skip entering a preferred slot (default: False).
    Returns:
        str: The validated user preferred slot.
    '''
    if allow_skip:
        slot = get_int_in_range("Enter Preferred Slot (0 to skip, 1-4): ", 0, 4)
        return None if slot == 0 else slot
    return get_int_in_range("Enter Preferred Slot (1-4): ", 1, 4)


def get_group_id() -> str | None:
    '''
    Get user's group ID for group requests. This field is optional.
    Returns:
        str | None: The user-entered group ID, or None if the user chooses to skip.
    '''
    return input("Enter Group ID (optional): ").strip() or None



def get_severity() -> int:
    '''
    Get and validate user's input for severity level in urgent service requests.
    Returns:
        int: The validated severity level.
    '''
    return get_int_in_range("Enter Severity (1-10): ", 1, 10)



def get_time_sensitivity() -> int:
    '''
    Get and validate user's input for time sensitivity in urgent service requests.
    Returns:
        int: The validated time sensitivity level.
    '''
    return get_int_in_range("Enter Time Sensitivity (1-10): ", 1, 10)



def get_crowd_level() -> int:
    '''
    Get and validate user's input for crowd level in urgent service requests.
    Returns:
        int: The validated crowd level.
    '''
    return get_int_in_range("Enter Crowd Level (1-10): ", 1, 10)



def get_description() -> str | None:
    '''
    Get user's description note for service requests. This field is optional.
    Returns:
        str | None: The user-entered description note, or None if the user chooses to skip.
    '''
    return input("Enter Description Note (optional): ").strip() or None


def normalize_input(user_input: str) -> str: 
    '''
    Normalize user input by converting it to a standard format\n
    e.g., "ai lab" → "AI_Lab"\n
    "hostel" → "Hostel"\n
    "urgent_service_request" → "Urgent_Service_Request".
    Args:
        user_input (str): The raw input from the user.
    Returns:
        str: The normalized user input.
    '''
    mapping = {
        'ai lab': 'AI Lab',  
    }

    normalized = mapping.get(user_input.lower(), user_input)
    return normalized.replace(" ", "_").title()
