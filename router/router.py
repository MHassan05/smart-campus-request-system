import utils.input_form as input_form
import random 

def generate_request_id() -> str:
    '''
    Generate a unique request ID for each user request.
    Returns:
        str: A unique request ID in the format "REQXXXX" where XXXX is a random 4-digit number.
    '''
    request_id = f"REQ{random.randint(1000, 9999)}"
    return request_id 


def route():
    user_input = input_form.get_user_input()
    request_type = user_input["request_type"]

    if request_type == "Navigation_Only":
        # TODO: Implement the logic to handle navigation-only requests
        pass 

    elif request_type == "Eligibility_Check":
        # TODO: Implement the logic to handle eligibility check requests
        pass

    elif request_type == "Booking_or_Scheduling":
        # TODO: Implement the logic to handle booking or scheduling requests
        pass

    elif request_type == "Urgent_Service_Request":
        # TODO: Implement the logic to handle urgent service requests
        pass 

    elif request_type == "Full_Service_Request":
        # TODO: Implement the logic to handle full service requests
        pass

    return None # TODO: Finalize the return value based on the implementation 

if __name__ == "__main__":
    route()

