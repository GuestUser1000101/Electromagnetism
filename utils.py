import numpy as np

def get_magnitude(vector: np.ndarray):
    return float(np.linalg.norm(vector))

def get_normalized(vector: np.ndarray, magnitude: float=1):
    prev_magnitude = get_magnitude(vector)
    return np.zeros(vector.shape) if prev_magnitude == 0 else vector / prev_magnitude * magnitude