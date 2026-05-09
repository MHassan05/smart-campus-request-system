from typing import Dict

ROLE_ENCODING: Dict[str, int] = {
    "Student":    0,
    "Instructor": 1,
    "Staff":      2
}

CATEGORY_ENCODING: Dict[str, int] = {
    "AI_Lab_Support": 0,
    "Viva":           1,
    "Access":         2,
    "Maintenance":    3,
    "Emergency_Help": 4
}

PRIORITY_LABELS = ["Low", "Normal", "High", "Urgent"]

FEATURE_ORDER = [
    "Role",
    "RequestType",
    "Severity",
    "TimeSensitivity",
    "CrowdLevel",
    "Distance",
    "Eligibility"
]


def build_feature_vector(processed_output: dict, distance: int, eligibility: bool) -> list:
    '''
    Build the numeric feature vector from processed request output.
    Args:
        processed_output (dict): The preprocessed request dictionary.
        distance (int): Estimated distance to destination.
        eligibility (bool): Whether the user is eligible.
    Returns:
        list: Numeric feature vector in fixed order.
    '''
    role       = ROLE_ENCODING.get(processed_output.get("role", "Student"), 0)
    req_type   = CATEGORY_ENCODING.get(processed_output.get("category", "AI_Lab_Support"), 0)
    severity   = processed_output.get("severity", 1)
    time_sens  = processed_output.get("time_sensitivity", 1)
    crowd      = processed_output.get("crowd_level", 1)
    elig       = 1 if eligibility else 0

    return [role, req_type, severity, time_sens, crowd, distance, elig]