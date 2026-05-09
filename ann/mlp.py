import math
from typing import List, Dict, Any

# ── Fixed weights (7 inputs → 4 hidden1 → 3 hidden2 → 4 outputs) ──────────────

# Hidden Layer 1: shape (4, 7) — 4 neurons, 7 inputs each
W1 = [
    [0.2, -0.1,  0.4,  0.35,  0.15, -0.1,  0.3],
    [0.1,  0.2,  0.3,  0.4,   0.1,  -0.2,  0.2],
    [0.3,  0.1,  0.35, 0.3,   0.2,  -0.15, 0.25],
    [0.15, 0.3,  0.25, 0.2,   0.3,  -0.05, 0.1],
]
B1 = [-1.0, -0.8, -0.9, -0.7]

# Hidden Layer 2: shape (3, 4)
W2 = [
    [0.4,  0.3,  0.35, 0.25],
    [0.3,  0.4,  0.2,  0.3],
    [0.25, 0.35, 0.4,  0.2],
]
B2 = [-0.5, -0.4, -0.6]

# Output Layer: shape (4, 3) — Low, Normal, High, Urgent
W3 = [
    [0.1,  0.2,  0.3],
    [0.3,  0.3,  0.2],
    [0.4,  0.35, 0.4],
    [0.5,  0.45, 0.5],
]
B3 = [-0.3, -0.4, -0.5, -0.6]

PRIORITY_LABELS = ["Low", "Normal", "High", "Urgent"]


def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def _softmax(values: List[float]) -> List[float]:
    exp_vals = [math.exp(v) for v in values]
    total    = sum(exp_vals)
    return [v / total for v in exp_vals]


def _forward(x: List[float], W: List[List[float]], b: List[float], activation=None) -> List[float]:
    output = []
    for i, (weights, bias) in enumerate(zip(W, b)):
        z = sum(w * xi for w, xi in zip(weights, x)) + bias
        output.append(_sigmoid(z) if activation else z)
    return output


def predict(feature_vector: List[float]) -> Dict[str, Any]:
    '''
    MLP multiclass classifier — predicts Low / Normal / High / Urgent.
    Args:
        feature_vector (List[float]): Numeric input vector [Role, RequestType, Severity,
                                      TimeSensitivity, CrowdLevel, Distance, Eligibility].
    Returns:
        Dict[str, Any]: Multiclass prediction result with confidence.
    '''
    h1         = _forward(feature_vector, W1, B1, activation="sigmoid")
    h2         = _forward(h1,             W2, B2, activation="sigmoid")
    raw_out    = _forward(h2,             W3, B3, activation=None)
    probs      = _softmax(raw_out)

    best_idx   = probs.index(max(probs))
    label      = PRIORITY_LABELS[best_idx]
    confidence = round(probs[best_idx], 4)

    return {
        "final_priority": label,
        "confidence":     confidence
    }