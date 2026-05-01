from graph_data import campus_unweighted_graph 

VALID_ROLES = ["student", "instructor", "staff"]
VALID_CATEGORIES = ["AI_Lab_Support", "Viva", "Access", "Maintenance"]
VALID_LOCATIONS = list(campus_unweighted_graph.keys())

REQUEST_TYPE_MAP = {
    "1": "Navigation_Only",
    "2": "Eligibility_Check",
    "3": "Booking_or_Scheduling",
    "4": "Urgent_Service_Request",
    "5": "Full_Service_Request"
}

# ------------------ BASIC HELPERS ------------------

def get_validated_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        for option in valid_options:
            if user_input == option.lower():
                return option
        print("Invalid input. Please try again.")


def get_int_in_range(prompt, min_value, max_value):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and min_value <= int(value) <= max_value:
            return int(value)
        print(f"Invalid input. Enter a number between {min_value} and {max_value}.")


def get_yes_no(prompt):
    while True:
        val = input(prompt).strip().lower()
        if val in ["yes", "no"]:
            return val
        print("Invalid input. Enter 'yes' or 'no'.")


def print_list(title, items):
    print(f"\n{title}:")
    for item in items:
        print(f"- {item}")


def validate_query(query):
    return "(" in query and ")" in query and len(query) > 3


# ------------------ FIELD FUNCTIONS ------------------

def get_name():
    name = input("Enter Name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter Name: ").strip()
    return name


def get_role():
    return get_validated_input(
        "Enter Role (student / instructor / staff): ",
        VALID_ROLES
    )


def get_category():
    print_list("Available Categories", VALID_CATEGORIES)
    return get_validated_input("Enter Category: ", VALID_CATEGORIES)


def get_location(prompt="Enter Location: "):
    print_list("Available Locations", VALID_LOCATIONS)
    return get_validated_input(prompt, VALID_LOCATIONS)


def get_preferred_slot(allow_skip=False):
    if allow_skip:
        slot = get_int_in_range("Enter Preferred Slot (0 to skip, 1-4): ", 0, 4)
        return None if slot == 0 else slot
    return get_int_in_range("Enter Preferred Slot (1-4): ", 1, 4)


def get_severity():
    return get_int_in_range("Enter Severity (1-10): ", 1, 10)


def get_time_sensitivity():
    return get_int_in_range("Enter Time Sensitivity (1-10): ", 1, 10)


def get_crowd_level():
    return get_int_in_range("Enter Crowd Level (1-10): ", 1, 10)


def get_query():
    while True:
        query = input("Enter Query (e.g. UsesLab(DrKhan, Lab1)): ").strip()
        if validate_query(query):
            return query
        print("Invalid query format.")


def get_group_id():
    return input("Enter Group ID (optional): ").strip() or None


def get_description():
    return input("Enter Description Note (optional): ").strip() or None


# ------------------ MAIN INPUT FUNCTION ------------------

def getInput():

    # --- Base Fields ---
    name = get_name()
    role = get_role()

    print("\nEnter Request Type:")
    for key, value in REQUEST_TYPE_MAP.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Enter Choice (1-5): ").strip()
        if choice in REQUEST_TYPE_MAP:
            request_type = REQUEST_TYPE_MAP[choice]
            break
        print("Invalid choice. Enter a number between 1 and 5.")

    # --- Initialize all fields ---
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

    # ------------------ CONDITIONAL INPUT ------------------

    if request_type == "Navigation_Only":
        current_location = get_location("Enter Current Location: ")
        destination = get_location("Enter Destination: ")

        while destination == current_location:
            print("Destination cannot be same as current location.")
            destination = get_location("Enter Destination: ")

    elif request_type == "Eligibility_Check":
        query = get_query()

    elif request_type == "Booking_or_Scheduling":
        category = get_category()
        preferred_slot = get_preferred_slot()
        group_id = get_group_id()

        if get_yes_no("Do you need route guidance? (yes/no): ") == "yes":
            current_location = get_location("Enter Current Location: ")

    elif request_type == "Urgent_Service_Request":
        category = get_category()
        current_location = get_location("Enter Current Location: ")

        severity = get_severity()
        time_sensitivity = get_time_sensitivity()
        crowd_level = get_crowd_level()
        preferred_slot = get_preferred_slot(allow_skip=True)

    elif request_type == "Full_Service_Request":
        category = get_category()
        current_location = get_location("Enter Current Location: ")

        preferred_slot = get_preferred_slot()
        severity = get_severity()
        time_sensitivity = get_time_sensitivity()
        crowd_level = get_crowd_level()
        description_note = get_description()

    # ------------------ FINAL STRUCTURED OUTPUT ------------------
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

# ------------------ MAIN ------------------
if __name__ == "__main__":
    user_input = getInput()
    print(user_input)