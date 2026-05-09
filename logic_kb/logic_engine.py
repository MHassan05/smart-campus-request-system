from aima3.logic import FolKB, expr
from typing import Dict, Any

FOL_FACTS = [
    "Teaches(DrKhan, AI)",
    "Enrolled(Ali, AI)",
    "Student(Ali)",
    "Student(Sara)",
    "Completed(Ali, ProgrammingFundamentals)"
]
FOL_RULES = [
    "Teaches(x, AI) ==> Instructor(x, AI)",
    "Instructor(x, AI) ==> UsesLab(x, Lab1)",
    "Enrolled(x, AI) ==> UsesLab(x, Lab1)",
    "Student(x) & Completed(x, ProgrammingFundamentals) ==> Eligible(x, AI)"
]

EXPLANATIONS = {
    "Instructor(DrKhan, AI)": [
        "Teaches(DrKhan, AI)",
        "Teaches(x, AI) ==> Instructor(x, AI)"
    ],
    "UsesLab(DrKhan, Lab1)": [
        "Teaches(DrKhan, AI)",
        "Teaches(x, AI) ==> Instructor(x, AI)",
        "Instructor(x, AI) ==> UsesLab(x, Lab1)"
    ],
    "UsesLab(Ali, Lab1)": [
        "Enrolled(Ali, AI)",
        "Enrolled(x, AI) ==> UsesLab(x, Lab1)"
    ],
    "Eligible(Ali, AI)": [
        "Student(Ali)",
        "Completed(Ali, ProgrammingFundamentals)",
        "Student(x) & Completed(x, ProgrammingFundamentals) ==> Eligible(x, AI)"
    ]
}

def get_explanation(query: str) -> list:
    '''
    Get the explanation for an entailed query from the EXPLANATIONS dictionary.
    
    Args:
        query (str): The query for which to get the explanation.
    Returns:
        list: A list of strings representing the explanation for the query.
    '''

    for key, explanation in EXPLANATIONS.items():
        if key.lower() == query.lower():
            return explanation

    return ["No explanation available for this query."]


def ask_query(query: str) -> Dict[str, Any]:
    '''
    Ask a query to the logic knowledge base and return the result.
    Args:
        query (str): The query to ask, in the format of a first-order logic expression.
    Returns:
        Dict[str, Any]: A dictionary containing the query, entailed status, and explanation.
    '''

    kb = FolKB()
    for fact in FOL_FACTS:
        kb.tell(expr(fact.lower()))
    for rule in FOL_RULES:
        kb.tell(expr(rule.lower()))

    result = kb.ask(expr(query.lower()))
    entailed = bool(result)

    return {
        "query":       query,
        "entailed":    entailed,
        "explanation": get_explanation(query) if entailed else []
    }

