import pygame
import numpy as np
from utils import *


class Renderable:
    def __init__(self):
        self.radius = 1
        self.color = pygame.Color(255, 255, 255)

    def render_circle(self, surface: pygame.Surface, pos: np.ndarray, thickness: int):
        pygame.draw.circle(surface, self.color, pos, self.radius, thickness)

    # https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame


class Player(Renderable):
    def __init__(self):
        super().__init__()
        self.radius = 5

        # Movement control
        self.pos = np.zeros(2)
        self.movement_vel = np.zeros(2)
        self.push_vel = np.zeros(2)
        self.max_speed = 130
        self.acceleration = 1400
        self.deadband = 10
        self.friction = 800
        self.mass = 1

        self.POSITIVE_COLOR = pygame.Color(242, 36, 84)
        self.NEGATIVE_COLOR = pygame.Color(150, 77, 240)
        self.NEUTRAL_COLOR = pygame.Color(234, 245, 193)

    def render(self, surface):
        self.render_circle(surface, self.pos, 0)

    def tick(self, up: bool, right: bool, down: bool, left: bool, delta_time: float):
        vertical = int(down) - int(up)
        horizontal = int(right) - int(left)

        movement_acc = get_normalized(np.array([horizontal, vertical])) * self.acceleration
        self.movement_vel += movement_acc * delta_time

        movement_speed = get_magnitude(self.movement_vel)
        if movement_speed > self.max_speed:
            self.movement_vel = get_normalized(self.movement_vel, self.max_speed)
        elif movement_speed <= self.deadband:
            self.movement_vel = np.zeros(2)

        net_vel = self.movement_vel + self.push_vel
        net_speed = get_magnitude(net_vel)
        if net_speed > 0:
            friction_acceleration = -get_normalized(net_vel) * self.friction
            self.movement_vel += friction_acceleration * get_magnitude(self.movement_vel) / net_speed * delta_time
            self.push_vel += friction_acceleration * get_magnitude(self.push_vel) /  net_speed * delta_time
            net_vel = self.movement_vel + self.push_vel

        self.pos += net_vel * delta_time

    def apply_force(self, force_vector, delta_time):
        self.push_vel += force_vector / self.mass * delta_time