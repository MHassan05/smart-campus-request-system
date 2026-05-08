from typing import Dict, Any, List, Optional
from csp.viva_csp import solve_viva, GROUPS

CATEGORY_ROOM_MAP: Dict[str, str] = {
    "AI_Lab_Support": "AI_Lab",
    "Viva":           "Seminar_Room",
    "Access":         "Library",
    "Maintenance":    "Exam_Hall",
}

SLOT_DOMAIN = [1, 2, 3, 4]

booked_slots: Dict[str, List[int]] = {
    "AI_Lab":       [],
    "Seminar_Room": [],
    "Library":      [],
    "Exam_Hall":    [],
}


def csp_assign(category: str, preferred_slot: int, group_id: Optional[str] = None) -> Dict[str, Any]:
    '''
    Assign a room and slot using CSP based on category.
    Args:
        category (str): The service category requested.
        preferred_slot (int): The user preferred slot (1-4).
        group_id (str | None): Group ID, required for Viva category.
    Returns:
        Dict[str, Any]: CSP assignment result.
    '''
    room = CATEGORY_ROOM_MAP.get(category)

    if room is None:
        return {
            "decision":      "rejected",
            "assigned_room": None,
            "assigned_slot": None,
            "destination":   None,
            "notes":         f"No room mapped for category '{category}'."
        }

    if category == "Viva":
        if group_id not in GROUPS:
            return {
                "decision":      "rejected",
                "assigned_room": None,
                "assigned_slot": None,
                "destination":   None,
                "notes":         f"Group '{group_id}' not found. Valid groups: {list(GROUPS.keys())}."
            }

        full_assignment = solve_viva()

        if full_assignment is None:
            return {
                "decision":      "rejected",
                "assigned_room": None,
                "assigned_slot": None,
                "destination":   None,
                "notes":         "No conflict-free viva schedule could be found."
            }

        assigned_slot = full_assignment[group_id]
        return {
            "decision":      "accepted",
            "assigned_room": room,
            "assigned_slot": assigned_slot,
            "destination":   room,
            "full_schedule": full_assignment,
            "notes":         f"Viva schedule solved. {group_id} assigned slot {assigned_slot}."
        }

    available_slots = [s for s in SLOT_DOMAIN if s not in booked_slots[room]]

    if not available_slots:
        return {
            "decision":      "rejected",
            "assigned_room": None,
            "assigned_slot": None,
            "destination":   None,
            "notes":         f"No available slots in {room}."
        }

    if preferred_slot in available_slots:
        assigned_slot = preferred_slot
        notes = f"Preferred slot {preferred_slot} assigned successfully."
    else:
        assigned_slot = available_slots[0]
        notes = f"Preferred slot {preferred_slot} unavailable. Slot {assigned_slot} assigned instead."

    booked_slots[room].append(assigned_slot)

    return {
        "decision":      "accepted",
        "assigned_room": room,
        "assigned_slot": assigned_slot,
        "destination":   room,
        "notes":         notes
    }