from ann import perceptron, mlp
from ann.ann_data import build_feature_vector
from typing import Dict, Any


def run_ann(processed_output: Dict[str, Any], distance: int, eligibility: bool) -> Dict[str, Any]:
    '''
    Run both Perceptron and MLP on the request and return combined priority output.
    Args:
        processed_output (Dict[str, Any]): The preprocessed request dictionary.
        distance (int): Estimated distance to destination.
        eligibility (bool): Whether the user passed logic check.
    Returns:
        Dict[str, Any]: Combined ANN output with binary and final priority.
    '''
    feature_vector = build_feature_vector(processed_output, distance, eligibility)

    perceptron_result = perceptron.predict(feature_vector)
    mlp_result        = mlp.predict(feature_vector)

    return {
        "feature_vector":  feature_vector,
        "binary_priority": perceptron_result["binary_priority"],
        "raw_score":       perceptron_result["raw_score"],
        "final_priority":  mlp_result["final_priority"],
        "confidence":      mlp_result["confidence"]
    }