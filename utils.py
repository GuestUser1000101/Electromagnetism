import numpy as np
import pygame


def get_magnitude(vector: np.ndarray):
    return float(np.linalg.norm(vector))


def get_normalized(vector: np.ndarray, magnitude: float = 1):
    prev_magnitude = get_magnitude(vector)
    return (
        np.zeros(vector.shape)
        if prev_magnitude == 0
        else vector / prev_magnitude * magnitude
    )


def get_gradient_color(color1: pygame.Color, color2: pygame.Color, amount: float, curve=lambda x: x):
    if amount < 0 or amount > 1:
        raise ValueError("Gradient amount should be between 0 and 1.")

    return pygame.Color(
        (
            color1.r + (color2.r - color1.r) * amount,
            color1.g + (color2.g - color1.g) * amount,
            color1.b + (color2.b - color1.b) * amount,
        )
    )
