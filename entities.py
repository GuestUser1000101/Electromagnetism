import pygame
import numpy as np
from utils import *
from itertools import combinations


class Renderable:
    renderables = set()

    def __init__(self):
        self.radius = 1
        self.color = pygame.Color(255, 255, 255)
        Renderable.renderables.add(self)

    def render_circle(self, surface: pygame.Surface, pos: np.ndarray, thickness: int):
        pygame.draw.circle(surface, self.color, pos, self.radius, thickness)

    # https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame


class Charge(Renderable):
    charges = set()
    FACTOR = 1
    COLORS = [pygame.Color(150, 77, 240), pygame.Color(234, 245, 193), pygame.Color(242, 36, 84)]

    def __init__(self, charge, initial_pos = np.zeros(2)):
        super().__init__()
        self.radius = 10

        self.pos = initial_pos
        self.vel = np.zeros(2)
        self.friction = 800
        self.charge = charge
        self.color = self.COLORS[np.sign(charge) + 1]
        self.mass = 1
        Charge.charges.add(self)
    
    def render(self, surface):
        self.render_circle(surface, self.pos, 3)

    def calculate_collision_dv(target, other):
        return ((2 * other.mass) / (target.mass  + other.mass)) * (np.dot(target.vel - other.vel, target.pos - other.pos) / get_magnitude(target.pos - other.pos)**2) * (other.pos - target.pos)


    def calculate_interactions(delta_time):
        for pair in combinations(Charge.charges, 2):
            dist = get_magnitude(pair[0].pos - pair[1].pos)

            if dist == 0:
                continue
            
            force = get_normalized(pair[0].pos - pair[1].pos) * pair[0].charge * pair[1].charge / dist**2
            pair[0].apply_force(force, delta_time)
            pair[1].apply_force(-force, delta_time)

            if dist <= pair[0].radius + pair[1].radius:
                pair[0].vel += Charge.calculate_collision_dv(pair[0], pair[1])
                pair[1].vel +=  Charge.calculate_collision_dv(pair[1], pair[0])
    
    def tick(self, delta_time):
        self.pos += self.vel * delta_time
    
    def apply_force(self, force_vector, delta_time):
        self.vel += force_vector / self.mass * delta_time

class Player(Renderable):
    players = set()

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
        Player.players.add(self)

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