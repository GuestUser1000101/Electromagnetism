import math
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

    def render_circle(self, surface: pygame.Surface, pos: np.ndarray, thickness: int, radius: 1):
        pygame.draw.circle(surface, self.color, pos, radius, thickness)

    # https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame


class Charge(Renderable):
    MAX_CHARGE = 200
    charges = set()
    FACTOR = 1
    COLORS = [pygame.Color(150, 77, 240), pygame.Color(226, 250, 192), pygame.Color(242, 36, 84)]

    def __init__(self, charge, initial_pos = np.zeros(2)):
        super().__init__()
        self.radius = 10

        self.pos = initial_pos
        self.vel = np.zeros(2)
        self.friction = 800
        self.set_charge(charge)
        self.mass = 1
        Charge.charges.add(self)
    
    def render(self, surface):
        self.render_circle(surface, self.pos, 3, self.radius)
    
    def calculate_wall_collision(self, wall_x, wall_y):
        if self.pos[0] <= self.radius or self.pos[0] >= wall_x - self.radius:
            self.vel[0] = -self.vel[0]
        if self.pos[1] <= self.radius or self.pos[1] >= wall_y - self.radius:
            self.vel[1] = -self.vel[1]

    def calculate_collision_dv(target, other):
        return ((2 * other.mass) / (target.mass  + other.mass)) * (np.dot(target.vel - other.vel, target.pos - other.pos) / get_magnitude(target.pos - other.pos)**2) * (other.pos - target.pos)

    def calculate_interactions(delta_time):
        for pair in combinations(Charge.charges, 2):
            dist = get_magnitude(pair[0].pos - pair[1].pos)

            if dist == 0:
                continue
            
            if dist <= pair[0].radius + pair[1].radius and (np.dot(pair[1].pos - pair[0].pos, pair[0].vel) > 0 or np.dot(pair[0].pos - pair[1].pos, pair[1].vel) > 0):
                dv0 = Charge.calculate_collision_dv(pair[0], pair[1])
                dv1 = Charge.calculate_collision_dv(pair[1], pair[0])
                
                pair[0].vel += dv0
                pair[1].vel += dv1
            else:
                force = get_normalized(pair[0].pos - pair[1].pos) * pair[0].charge * pair[1].charge / dist**2

                pair[0].apply_force(force, delta_time)
                pair[1].apply_force(-force, delta_time)

    def set_charge(self, charge):
        self.charge = charge
        if self.charge > 0:
            self.color = get_gradient_color(Charge.COLORS[1], Charge.COLORS[2], self.charge / Charge.MAX_CHARGE, lambda x: math.sqrt(x * (2 - x)))
        else:
            self.color = get_gradient_color(Charge.COLORS[1], Charge.COLORS[0], -self.charge / Charge.MAX_CHARGE, lambda x: math.sqrt(x * (2 - x)))

    def tick(self, delta_time):
        self.pos += self.vel * delta_time
    
    def apply_force(self, force_vector, delta_time):
        self.vel += force_vector / self.mass * delta_time

class Player(Renderable):
    players = set()

    def __init__(self):
        super().__init__()
        self.radius = 5
        self.affect_radius = 100

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
        self.render_circle(surface, self.pos, 0, self.radius)
        self.render_circle(surface, self.pos, 1, self.affect_radius)

    def tick(self, up, right, down, left, interact, delta_time):
        if interact.is_pressed:
            for charge in Charge.charges:
                if get_magnitude(charge.pos - self.pos) <= self.affect_radius:
                    charge.set_charge(-charge.charge)

        vertical = int(down.is_held) - int(up.is_held)
        horizontal = int(right.is_held) - int(left.is_held)

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