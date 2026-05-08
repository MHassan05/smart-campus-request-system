import utils.input_form as input_form
from utils.preprocess import preprocess_request
from router.handler import navigate_only, eligibility_check, booking_or_scheduling
from utils.helper import print_dict
import random 
from typing import *

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
    request_id = generate_request_id()
    processed_output = preprocess_request(user_input, request_id)
    request_type = processed_output["request_type"]

   
    if request_type == "Navigation_Only":
        searched_output = navigate_only(processed_output)
        print_dict(searched_output, "Search Output")
        return {
            "request_id": "REQ401",
            "decision": "completed",
            "route": {
                **searched_output
            },
            "message": "Best route generated successfully."
        }

    elif request_type == "Eligibility_Check":
        eligibility_output = eligibility_check(processed_output) 
        print_dict(eligibility_output, "Eligibility Check Output")
        return {
            "request_id": "REQ402",
            "decision": "answered" if eligibility_output["entailed"] else "rejected",
            "eligibility": {
                **eligibility_output
            },
            "message": "Eligibility check answered successfully." if eligibility_output["entailed"] else "Eligibility check failed."
        }
    
    elif request_type == "Booking_or_Scheduling":
        booking_output = booking_or_scheduling(processed_output)
        print_dict(booking_output, "Booking Output")

        assignment = booking_output.get("assignment") or {}
        route      = booking_output.get("route") or {}

        return {
            "request_id":  request_id,
            "decision":    booking_output["decision"],
            "eligibility": {
                "allowed":     booking_output["eligibility"].get("allowed", False),
                "explanation": booking_output["eligibility"].get("explanation", "")
            },
            "assignment": {
                "room": assignment.get("assigned_room"),
                "slot": assignment.get("assigned_slot")
            },
            "route":    route,
            "message": (
                f"Booking accepted. You are assigned {assignment.get('assigned_room')} in slot {assignment.get('assigned_slot')}."
                if booking_output["decision"] == "accepted"
                else "Booking request rejected."
            )
        }

    elif request_type == "Urgent_Service_Request":
        # TODO: Implement the logic to handle urgent service requests
        pass 

    elif request_type == "Full_Service_Request":
        # TODO: Implement the logic to handle full service requests
        pass

    return None # TODO: Finalize the return value based on the implementation

if __name__ == "__main__":
    route()

