import math
import pygame
from particles.particle import Particle
from particles.vector2d import Vector2D

particle_radius = 2
start_velocity_multiplication = 3
spawn_circle_radius = 100
spawn_circle_start_angle = 1
spawn_circle_end_angle = 360
particles_amount = 50


class Bag:
    def __init__(self, pos):
        self.pos = pos
        self.particles = []

    def init_particles(self):
        par = []
        for i in range(spawn_circle_start_angle, spawn_circle_end_angle,
                       int((spawn_circle_end_angle - spawn_circle_start_angle) / particles_amount)):
            v = Vector2D()
            v.x = math.cos(math.radians(i)) * start_velocity_multiplication
            v.y = math.sin(math.radians(i)) * start_velocity_multiplication
            par.append(self.create_particle(i, v))
        return par

    def create_particle(self, i, v):
        return Particle(
                    Vector2D(self.pos.x + math.cos(math.radians(i)) * spawn_circle_radius,
                             self.pos.y + math.sin(math.radians(i)) * spawn_circle_radius),
                    v, particle_radius)

    def throw_particles(self, screen, boundaries, fps):
        for p in self.particles:
            if pygame.display.get_surface().get_size()[0] > p.center.x > 0 and \
                    pygame.display.get_surface().get_size()[1] > p.center.y > 0:
                p.draw(screen, boundaries, self.particles, fps)
            else:
                self.particles.remove(p)

    def update(self, dx, dy):
        self.pos.x = dx
        self.pos.y = dy

    def add_more_particles(self):
        self.particles += self.init_particles()

    def update_and_throw_particles(self, screen, dx, dy, boundaries, fps):
        self.update(dx, dy)
        self.throw_particles(screen, boundaries, fps)
