import math
import pygame
from particles.vector2d import Vector2D

particle_collide = True
boundary_collide = True
use_gravity = False
gravity = 9.81
loose_velocity_based_on_angle = True
"""
Specifies how much of velocity is lost when hitting a wall at 90' angle. 
Velocity loss will be equally spread from 1 - 90 degree angle hit - loosing least velocity at 1' hit and max at 90' hit
value(1) - all velocity will be lost on perpendicular hit, value(0.1) - almost no velocity lost on perpendicular

Note: for this to work *loose_velocity_based_on_angle* must be set to True!
"""
velocity_loss_on_90_degree_collision = 0.8


def sub(v1, v2):
    return Vector2D(v1.x - v2.x, v1.y - v2.y)


def dot(v1, v2):
    vx = v1.x * v2.x
    vy = v1.y * v2.y
    return vx + vy


def magnitude(v):
    return (v.x ** 2 + v.y ** 2) ** 0.5


def multiply(v, c):
    return Vector2D(v.x * c, v.y * c)


def distance(p1, p2):
    return (int(p1.x - p2.x) ** 2 + int(p1.y - p2.y) ** 2) ** 0.5


def add(v1, v2):
    return Vector2D(v1.x + v2.x, v1.y + v2.y)


def normalise(v):
    length = magnitude(v)
    length = 1 if length == 0 else length
    v.x /= length
    v.x /= length
    return v


def project(v1, v2):
    scale = dot(v1, v2) / (magnitude(v2) ** 2)
    return Vector2D(v2.x * scale, v2.y * scale)


"""
Returns velocity of particle p1 after colliding with particle p2
"""


def velocity_after_collision(p1, p2):
    t1 = sub(p1.velocity, p2.velocity)
    t2 = sub(p1.center, p2.center)
    top = dot(t1, t2)
    bot = magnitude(sub(p1.center, p2.center)) ** 2
    u = top / bot
    return sub(p1.velocity, multiply(t2, u))


class Particle:
    def __init__(self, center, velocity, radius):
        self.center = center
        self.birth = pygame.time.get_ticks()
        self.velocity = velocity
        self.color = (255, 255, 255)
        self.radius = radius
        self.mass = self.radius ** 2

    def draw(self, screen, boundaries, particles, fps):
        self.update_color()
        self.detect_collisions(boundaries, particles)
        self.move(fps)
        pygame.draw.circle(screen, self.color, (int(self.center.x), int(self.center.y)), self.radius, self.radius)

    def update_color(self):
        red = (abs(self.velocity.x) + abs(self.velocity.y)) * 100
        red = 255 if red > 255 else red
        self.color = (red, 130, 130)

    def detect_collisions(self, boundaries, particles):
        if particle_collide:
            self.particles_collision(particles)
        if boundary_collide:
            self.boundary_collisions(boundaries)

    def move(self, fps):
        self.center = add(self.center, self.velocity)
        self.loose_some_velocity(loss_x=0.9999, loss_y=0.9999)
        self.gravity(fps)

    def particles_collision(self, particles):
        for p in particles:
            if p != self and self.particle_intersect(p):
                self.collision_with(p)

    def collision_with(self, particle):
        self_velocity = velocity_after_collision(self, particle)
        particle_velocity = velocity_after_collision(particle, self)
        self.velocity = self_velocity
        particle.velocity = particle_velocity

    def boundary_collisions(self, boundaries):
        for bound in boundaries:
            if self.boundary_intersect(bound):
                v = Vector2D(math.cos(math.radians(90 + bound.angle)), math.sin(math.radians(90 + bound.angle)))
                to_sub = multiply(normalise(v), 2 * dot(self.velocity, v))

                if loose_velocity_based_on_angle:
                    cos_angle = abs(dot(self.velocity, v) / (magnitude(v) * magnitude(self.velocity)))
                    cos_angle *= velocity_loss_on_90_degree_collision
                    cos_angle = 1 - cos_angle
                    self.velocity = sub(self.velocity, to_sub)
                    self.loose_some_velocity(loss_x=cos_angle, loss_y=cos_angle)
                else:
                    self.velocity = sub(self.velocity, to_sub)
                    self.loose_some_velocity()

    def particle_intersect(self, c2):
        dist = distance(self.center, c2.center)
        r_sum = self.radius + c2.radius
        return dist <= r_sum

    # Workaround for checking if circle intersects with a line.
    # This is done by line intersection because vector projection which was not precise... or poorly used :)
    def boundary_intersect(self, bound):
        x1 = self.center.x
        y1 = self.center.y

        v_len = magnitude(self.velocity)
        scale = self.radius / v_len
        if scale > 1:
            scaled_v = multiply(self.velocity, scale)
        else:
            scaled_v = self.velocity
        x2 = self.center.x + scaled_v.x
        y2 = self.center.y + scaled_v.y

        x3 = bound.start.x
        y3 = bound.start.y

        x4 = bound.end.x
        y4 = bound.end.y

        divider = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if divider == 0:
            return False
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / divider
        u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / divider

        return 1 >= t >= 0 >= u >= -1

    def loose_some_velocity(self, loss_x=0.7, loss_y=0.7):
        self.velocity.x *= loss_x
        self.velocity.y *= loss_y

    def gravity(self, fps):
        if use_gravity:
            if fps > 0:
                self.velocity.y += gravity / fps
