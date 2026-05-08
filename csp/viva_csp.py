from typing import Dict, Optional

GROUPS = {
    "G1": {"examiner": "DrKhan",  "supervisor": "DrAli"},
    "G2": {"examiner": "DrSaeed", "supervisor": "DrAli"},
    "G3": {"examiner": "DrKhan",  "supervisor": "DrRaza"},
    "G4": {"examiner": "DrRaza",  "supervisor": "DrSaeed"},
    "G5": {"examiner": "DrSaeed", "supervisor": "DrAli"},
    "G6": {"examiner": "DrKhan",  "supervisor": "DrRaza"},
}

SLOT_DOMAIN = [1, 2, 3, 4]

CONSTRAINTS = {
    "slot_conflict":    [("G1","G2"), ("G1","G4"), ("G2","G4"), ("G3","G5"), ("G3","G6"), ("G5","G6")],
    "examiner_clash":   [("G1","G3")],
    "supervisor_clash": [("G2","G5")],
    "precedence":       [("G4","G3")],
}


def _is_consistent(group: str, slot: int, assignment: Dict[str, int]) -> bool:
    for constraint_type in ["slot_conflict", "examiner_clash", "supervisor_clash"]:
        for (a, b) in CONSTRAINTS[constraint_type]:
            if group == a and assignment.get(b) == slot:
                return False
            if group == b and assignment.get(a) == slot:
                return False

    for (earlier, later) in CONSTRAINTS["precedence"]:
        if group == later and earlier in assignment:
            if assignment[earlier] >= slot:
                return False
        if group == earlier and later in assignment:
            if slot >= assignment[later]:
                return False

    return True


def solve_viva() -> Optional[Dict[str, int]]:
    '''
    Backtracking CSP solver for Viva scheduling.
    Returns:
        Dict[str, int]: Conflict-free slot assignment for all groups, or None.
    '''
    groups = list(GROUPS.keys())
    assignment: Dict[str, int] = {}

    def backtrack(index: int) -> bool:
        if index == len(groups):
            return True
        group = groups[index]
        for slot in SLOT_DOMAIN:
            if _is_consistent(group, slot, assignment):
                assignment[group] = slot
                if backtrack(index + 1):
                    return True
                del assignment[group]
        return False

    return assignment if backtrack(0) else None