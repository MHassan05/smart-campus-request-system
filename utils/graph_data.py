campus_unweighted_graph = {
    "Medical_Center": ["Bus_Stop", "Hostel"],
    "Bus_Stop": ["Medical_Center", "Main_Gate", "Parking"],
    "Main_Gate": ["Bus_Stop", "Admin_Block", "Parking", "Hostel"],
    "Admin_Block": ["Main_Gate", "Student_Services", "Exam_Hall"],
    "Parking": ["Bus_Stop", "Main_Gate", "Science_Block"],
    "Hostel": ["Medical_Center", "Main_Gate", "Cafeteria"],
    "Student_Services": ["Admin_Block", "Library"],
    "Exam_Hall": ["Admin_Block", "Science_Block", "Seminar_Room"],
    "Science_Block": ["Parking", "Exam_Hall", "Cafeteria", "AI_Lab", "Seminar_Room"],
    "Cafeteria": ["Hostel", "Science_Block", "Library"],
    "Seminar_Room": ["Exam_Hall", "Science_Block"],
    "AI_Lab": ["Science_Block", "Library"],
    "Library": ["Student_Services", "Cafeteria", "AI_Lab"]
}

campus_weighted_graph = {
    "Main_Gate": {
        "Admin_Block": 4, "Parking": 2, "Bus_Stop": 1, "Hostel": 5
        },
    "Admin_Block": {
        "Main_Gate": 4, "Student_Services": 1, "Exam_Hall": 2
        },
    "Student_Services": {
        "Admin_Block": 1, "Library": 2
        },
    "Exam_Hall": {
        "Admin_Block": 2, "Seminar_Room": 1, "Science_Block": 3
        },
    "Seminar_Room": {
        "Exam_Hall": 1, "Science_Block": 2
        },
    "Parking": {
        "Main_Gate": 2, "Bus_Stop": 2, "Science_Block": 3
    },
    "Bus_Stop": {
        "Main_Gate": 1, "Parking": 2, "Medical_Center": 2
    },
    "Medical_Center": {
        "Bus_Stop": 2, "Hostel": 3
    },
    "Hostel": {
        "Main_Gate": 5, "Medical_Center": 3, "Cafeteria": 2
    },
    "Cafeteria": {
        "Hostel": 2, "Library": 2, "Science_Block": 3
    },
    "Library": {
        "Student_Services": 2, "Cafeteria": 2, "AI_Lab": 3
    },
    "Science_Block": {
        "Parking": 3, "Exam_Hall": 3, "Seminar_Room": 2, "Cafeteria": 3, "AI_Lab": 1
    },
    "AI_Lab": {
        "Library": 3, "Science_Block": 1
    }
}

heuristics = {
    "Main_Gate": (0, 4),
    "Admin_Block": (3, 5),
    "Student_Services": (6, 5),
    "Exam_Hall": (8, 5),
    "Seminar_Room": (10, 4),
    "Parking": (2, 4),
    "Bus_Stop": (0, 1),
    "Medical_Center": (1, 1),
    "Hostel": (2, 0),
    "Cafeteria": (4, 1),
    "Library": (6, 2),
    "Science_Block": (7, 1),
    "AI_Lab": (9, 2)
}