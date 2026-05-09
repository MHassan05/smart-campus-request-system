import math
from typing import List, Dict, Any

# Weights for w1-w7 and bias — tuned for urgency detection
WEIGHTS = [0.1, 0.1, 0.4, 0.35, 0.15, -0.1, 0.2]
BIAS    = -4.5
THRESHOLD = 0.5


def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def predict(feature_vector: List[float]) -> Dict[str, Any]:
    '''
    Perceptron binary classifier — predicts urgent vs not_urgent.
    Args:
        feature_vector (List[float]): Numeric input vector [Role, RequestType, Severity,
                                      TimeSensitivity, CrowdLevel, Distance, Eligibility].
    Returns:
        Dict[str, Any]: Binary prediction result.
    '''
    weighted_sum = sum(w * x for w, x in zip(WEIGHTS, feature_vector)) + BIAS
    output       = _sigmoid(weighted_sum)
    label        = "urgent" if output >= THRESHOLD else "not_urgent"

    return {
        "binary_priority": label,
        "raw_score":       round(output, 4)
    }

