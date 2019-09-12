import math
import pygame
from particles.vector2d import Vector2D

particles_collide = True
boundary_collide = True
use_gravity = False
gravity = 9.81
loose_momentum_based_on_angle = True
"""
Specifies how much of velocity is lost when hitting a wall at 90' angle. 
Velocity loss will be equally spread from 1 - 90 degree angle hit - loosing least velocity at 1' hit and max at 90' hit
value(1) - all velocity will be lost on perpendicular hit, value(0.1) - almost no velocity lost on perpendicular

Note: for this to work *loose_momentum_based_on_angle* must be set to True!
"""
momentum_loss_on_90_degree_collision = 0.8


def sub(v1, v2):
    s = Vector2D(v1.x - v2.x, v1.y - v2.y)
    return s


def dot(v1, v2):
    vs = v1.x * v2.x
    vx = v1.y * v2.y
    return vs + vx


def magnitude(v1):
    return (v1.x ** 2 + v1.y ** 2) ** 0.5


def multiply(v, c):
    return Vector2D(v.x * c, v.y * c)


def distance(p1, p2):
    return (int(p1.x - p2.x) ** 2 + int(p1.y - p2.y) ** 2) ** 0.5


def add(v1, v2):
    v = Vector2D()
    v.x = v1.x + v2.x
    v.y = v1.y + v2.y
    return v


def normalise(v):
    length = magnitude(v)
    length = 1 if length == 0 else length
    v.x /= length
    v.x /= length
    return v


def project(v1, v2):
    scale = dot(v1, v2) / (magnitude(v2) ** 2)
    return Vector2D(v2.x * scale, v2.y * scale)


def intersect(c1, c2):
    dist = distance(c1.center, c2.center)
    r_sum = c1.radius + c2.radius
    return dist <= r_sum


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
        self.detect_col(boundaries, particles)
        self.move(fps)
        pygame.draw.circle(screen, self.color, (int(self.center.x), int(self.center.y)), self.radius, self.radius)

    def update_color(self):
        red = (abs(self.velocity.x) + abs(self.velocity.y)) * 100
        red = 255 if red > 255 else red
        self.color = (red, 130, 130)

    def move(self, fps):
        self.center = add(self.center, self.velocity)
        self.loose_some_momentum(loss_x=0.9999, loss_y=0.9999)
        self.gravity(fps)

    def start_calculating_collision(self, particles):
        for p in particles:
            if p != self and intersect(self, p):
                self.collision_with(p)

    def collision_with(self, ball):
        my_velocity = self.self_velocity_after_collision(ball)
        your_velocity = self.collided_ball_velocity_after_collision(ball)
        self.velocity = my_velocity
        ball.velocity = your_velocity

    def self_velocity_after_collision(self, ball):
        t1 = sub(self.velocity, ball.velocity)
        t2 = sub(self.center, ball.center)
        top = dot(t1, t2)
        bot = magnitude(sub(self.center, ball.center)) ** 2
        u = top / bot
        return sub(self.velocity, multiply(t2, u))

    def collided_ball_velocity_after_collision(self, ball):
        t1 = sub(ball.velocity, self.velocity)
        t2 = sub(ball.center, self.center)
        top = dot(t2, t1)
        bot = magnitude(sub(ball.center, self.center)) ** 2
        u = top / bot
        return sub(ball.velocity, multiply(t2, u))

    def detect_col(self, boundaries, particles):
        if particles_collide:
            self.start_calculating_collision(particles)
        if boundary_collide:
            for bound in boundaries:
                if self.is_intersecting(bound):
                    v = Vector2D(math.cos(math.radians(90 + bound.angle)), math.sin(math.radians(90 + bound.angle)))
                    to_sub = multiply(normalise(v), 2 * dot(self.velocity, v))

                    if loose_momentum_based_on_angle:
                        cos_angle = abs(dot(self.velocity, v) / (magnitude(v) * magnitude(self.velocity)))
                        cos_angle *= momentum_loss_on_90_degree_collision
                        cos_angle = 1 - cos_angle
                        self.velocity = sub(self.velocity, to_sub)
                        self.loose_some_momentum(loss_x=cos_angle, loss_y=cos_angle)
                    else:
                        self.velocity = sub(self.velocity, to_sub)
                        self.loose_some_momentum()

    # Workaround for checking if circle intersects with a line.
    # This is done by line intersection because vector projection which was not precise... or not used correctly :)
    def is_intersecting(self, bound):
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

        diff = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if diff == 0:
            return False
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / diff
        u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / diff

        return 1 >= t >= 0 >= u >= -1

    def loose_some_momentum(self, loss_x=0.7, loss_y=0.7):
        self.velocity.x *= loss_x
        self.velocity.y *= loss_y

    def gravity(self, fps):
        if use_gravity:
            if fps > 0:
                self.velocity.y += gravity / fps
