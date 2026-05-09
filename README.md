# Smart Campus Request System

A CLI-based AI decision support system for managing campus service requests.
The system routes structured requests through intelligent pipelines using
Search Algorithms, Logic/Knowledge Base, Constraint Satisfaction, and
Artificial Neural Networks.

---

## Project Structure

```
smart-campus-request-system/
│
├── main.py                  # Entry point
│
├── router/
│   ├── router.py            # Request routing and final response
│   └── handler.py           # Pipeline handlers for each request type
│
├── utils/
│   ├── input_form.py        # CLI input collection and validation
│   ├── preprocess.py        # Request preprocessing and normalization
│   ├── helper.py            # Shared helper functions
│   └── graph_data.py        # Campus graph definitions and heuristics
│
├── searching_algorithms/
│   ├── BFS.py               # Breadth-First Search
│   ├── A_STAR.py            # A* Search with Euclidean heuristic
│   └── UCS.py               # Uniform Cost Search
│
├── logic_kb/
│   └── logic_engine.py      # FOL Knowledge Base and inference engine
│
├── csp/
│   ├── csp_solver.py        # CSP interface for all categories
│   └── viva_csp.py          # Backtracking CSP solver for Viva scheduling
│
└── ann/
    ├── ann_engine.py        # Public ANN interface
    ├── ann_data.py          # Feature encodings and vector builder
    ├── perceptron.py        # Binary classifier: urgent vs not_urgent
    └── mlp.py               # Multiclass classifier: Low/Normal/High/Urgent
```

---

## Request Types and Pipelines

| Request Type | Pipeline |
|---|---|
| Navigation_Only | Search |
| Eligibility_Check | Logic/KB |
| Booking_or_Scheduling | Logic/KB → CSP → optional Search |
| Urgent_Service_Request | ANN → Logic/KB → CSP → Search |
| Full_Service_Request | ANN → Logic/KB → CSP → Search |

---

## Modules

### Search Module
Handles campus navigation using three algorithms:
- **BFS** — for unweighted graph (shortest hops)
- **A\*** — for weighted graph with Euclidean heuristic
- **UCS** — for weighted graph without heuristic

### Logic / Knowledge Base
First-order logic inference using `aima3.FolKB`.
Checks eligibility and access permissions based on
predefined facts and rules.

### CSP Module
Constraint Satisfaction Problem solver for scheduling:
- **Viva** — backtracking solver with slot conflict,
  examiner clash, supervisor clash, and precedence constraints
- **Other categories** — conflict-free slot and room assignment

### ANN Module
Priority prediction using two models:
- **Perceptron** — binary baseline (urgent / not_urgent)
- **MLP** — multiclass operational model (Low / Normal / High / Urgent)

Feature vector order: `[Role, RequestType, Severity, TimeSensitivity, CrowdLevel, Distance, Eligibility]`

---

## How to Run

```bash
pip install aima3
python main.py
```

---

## Example: Full Service Request
Name: Ali  
Role: Student  
Request Type: Full_Service_Request  
Category: AI_Lab_Support  
Current Location: Hostel  
Preferred Slot: 2  
Severity: 8  
Time Sensitivity: 9   
Crowd Level: 5  
Expected output includes ANN priority prediction, logic
eligibility check, CSP room and slot assignment, and
A* route from Hostel to AI_Lab.

---

## Team

| Name | Email | GitHub |
|---|---|---|
| Muhammad Zain Kamal | zain.kamal2003@gmail.com | [ZNLAIG](https://github.com/ZNLAIG) |
| Hamza Shabbir | hamzashabbirhs0123@gmail.com | [Hamza-s2004](https://github.com/Hamza-s2004) |
| Muhammad Hassan | m.hassan.x05@gmail.com | [MHassan05](https://github.com/MHassan05) |

---

## Course
Artificial Intelligence Lab — Semester Project  
Department of Computer Science
