def getInput(): 

    try: 
        name = input("Enter Name: ")
        role = input("Enter Role: ")

        print("Enter Request Type: ")
        print("1. Navigation_Only")
        print("2. Eligibility_Check")
        print("3. Booking_or_Scheduling")
        print("4. Urgent_Service_Request")
        print("5. Full_Service_Request")
        request_type = int(input("Enter Choice (1-5): ")) 

        category = input("Enter Category (AI_Lab_Support / Viva / Access / Maintenance):")
        current_location = input("Enter Current Location: ")
        destination = input("Enter Destination: ")
        preferred_slots = int(input("Enter preferred slots(1-4): "))
        severity = int(input("Enter Severity (1-10): "))
        time_sensitivity = int(input("Enter Time Sensitivity (1-10): "))
        crowd_level = int(input("Enter Crowd Level (1-10): "))
        description = input("Enter Description Note (optional): ")
        
        return {
            "name": name,
            "role": role,
            "request_type": request_type,
            "category": category,
            "current_location": current_location,
            "destination": destination,
            "preferred_slots": preferred_slots,
            "severity": severity,
            "time_sensitivity": time_sensitivity,
            "crowd_level": crowd_level,
            "description": description
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    





