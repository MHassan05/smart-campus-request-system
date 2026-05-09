import math
from typing import List, Dict, Any

# Hidden Layer 1: shape (4, 7)
# High weights on Severity(x3) and TimeSensitivity(x4)
W1 = [
    [0.02, 0.02, 0.8,  0.75, 0.3,  -0.1,  0.35],
    [0.02, 0.02, 0.75, 0.7,  0.25, -0.1,  0.3 ],
    [0.02, 0.02, 0.65, 0.6,  0.35, -0.05, 0.25],
    [0.02, 0.02, 0.55, 0.5,  0.4,  -0.05, 0.2 ],
]
# Biases calibrated so neuron fires only when severity+time_sensitivity > ~6
B1 = [-5.5, -5.1, -4.7, -4.3]

# Hidden Layer 2: shape (3, 4)
W2 = [
    [0.8,  0.7,  0.75, 0.65],
    [0.65, 0.75, 0.55, 0.7 ],
    [0.55, 0.65, 0.8,  0.5 ],
]
B2 = [-1.8, -1.5, -1.9]

# Output Layer: shape (4, 3) — Low, Normal, High, Urgent
# Strongly separated — high h2 activation → Urgent, low → Low
W3 = [
    [-1.5, -1.3, -1.6],   # Low
    [-0.6, -0.4, -0.7],   # Normal
    [ 0.7,  0.8,  0.6],   # High
    [ 1.8,  1.7,  1.9],   # Urgent
]
B3 = [1.8, 0.5, -0.8, -2.2]

PRIORITY_LABELS = ["Low", "Normal", "High", "Urgent"]


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def softmax(values: List[float]) -> List[float]:
    exp_vals = [math.exp(v) for v in values]
    total    = sum(exp_vals)
    return [v / total for v in exp_vals]


def forward(x: List[float], W: List[List[float]], b: List[float], activation=None) -> List[float]:
    output = []
    for i, (weights, bias) in enumerate(zip(W, b)):
        z = sum(w * xi for w, xi in zip(weights, x)) + bias
        output.append(sigmoid(z) if activation else z)
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
    h1         = forward(feature_vector, W1, B1, activation="sigmoid")
    h2         = forward(h1,             W2, B2, activation="sigmoid")
    raw_out    = forward(h2,             W3, B3, activation=None)
    probs      = softmax(raw_out)

    best_idx   = probs.index(max(probs))
    label      = PRIORITY_LABELS[best_idx]
    confidence = round(probs[best_idx], 4)

    return {
        "final_priority": label,
        "confidence":     confidence
    }