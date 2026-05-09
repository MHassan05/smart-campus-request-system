import utils.input_form as input_form
from utils.preprocess import preprocess_request
from router.handler import (navigate_only, eligibility_check, booking_or_scheduling,
                             urgent_service_request, full_service_request)
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


def route() -> Optional[Dict[str, Any]]:
    '''
    Main routing function that collects user input, preprocesses it, and dispatches
    it to the appropriate handler based on request type.
    Returns:
        Optional[Dict[str, Any]]: The final response dictionary, or None if unhandled.
    '''
    user_input = input_form.get_user_input()
    request_id = generate_request_id()
    processed_output = preprocess_request(user_input, request_id)
    request_type = processed_output["request_type"]

   
    if request_type == "Navigation_Only":
        searched_output = navigate_only(processed_output)
        print_dict(searched_output, "Search Output")
        return {
            "request_id": request_id,
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
            "request_id": request_id,
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
        output = urgent_service_request(processed_output)
        ann        = output["ann"]
        eligibility = output["eligibility"]
        csp        = output["csp"]
        route      = output["route"]

        if not eligibility["allowed"] or (csp and csp["decision"] == "rejected"):
            return {
                "request_id": request_id,
                "decision":   "rejected",
                "priority":   ann,
                "eligibility": eligibility,
                "message":    "Your urgent request was rejected."
            }

        response = {
            "request_id":  request_id,
            "decision":    "accepted",
            "priority": {
                "binary_priority": ann["binary_priority"],
                "final_priority":  ann["final_priority"],
                "confidence":      ann["confidence"]
            },
            "eligibility": eligibility,
            "assignment": {
                "room":  csp["assigned_room"],
                "slot":  csp["assigned_slot"],
                "notes": csp["notes"]
            },
            "message": f"Urgent request accepted. Assigned {csp['assigned_room']} slot {csp['assigned_slot']}."
        }

        if route:
            response["route"] = route

        return response 

    elif request_type == "Full_Service_Request":
        output = full_service_request(processed_output)
        ann         = output["ann"]
        eligibility = output["eligibility"]
        csp         = output["csp"]
        route       = output["route"]

        if not eligibility["allowed"] or (csp and csp["decision"] == "rejected"):
            return {
                "request_id":  request_id,
                "decision":    "rejected",
                "priority":    ann,
                "eligibility": eligibility,
                "message":     "Your full service request was rejected."
            }

        return {
            "request_id": request_id,
            "decision":   "accepted",
            "priority": {
                "binary_priority": ann["binary_priority"],
                "final_priority":  ann["final_priority"],
                "confidence":      ann["confidence"]
            },
            "eligibility": eligibility,
            "assignment": {
                "room":  csp["assigned_room"],
                "slot":  csp["assigned_slot"],
                "notes": csp["notes"]
            },
            "route":    route,
            "message":  f"Full service accepted. Assigned {csp['assigned_room']} slot {csp['assigned_slot']}. Follow the route guidance."
        }

    return None 

if __name__ == "__main__":
    route()

