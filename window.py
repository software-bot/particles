import math
import random
import pygame
from particles.boundary import Boundary
from particles.bag import Bag
from particles.vector2d import Vector2D


def is_running(particle):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            particle.reset()
    return True


def random_boundaries():
    for i in range(10):
        x = random.randrange(100, pygame.display.get_surface().get_size()[0] - 100, 1)
        y = random.randrange(100, pygame.display.get_surface().get_size()[1] - 100, 1)
        angle = random.randrange(0, 360, 1)
        length = random.randrange(100, 500, 20)
        boundaries.append(
            Boundary(Vector2D(x, y),
                     Vector2D(x + math.cos(math.radians(angle)) * length, y + math.sin(math.radians(angle)) * length),
                     angle))


def tube():
    boundaries.append(
        Boundary(Vector2D(410, 100),
                 Vector2D(410 + math.cos(math.radians(90)) * 600, 100 + math.sin(math.radians(90)) * 600),
                 90))

    boundaries.append(
        Boundary(Vector2D(550, 100),
                 Vector2D(550 + math.cos(math.radians(90)) * 600, 100 + math.sin(math.radians(90)) * 600),
                 90))

    boundaries.append(
        Boundary(Vector2D(410 + math.cos(math.radians(90)) * 600, 100 + math.sin(math.radians(90)) * 600),
                 Vector2D(630 + math.cos(math.radians(90)) * 600, 100 + math.sin(math.radians(90)) * 600),
                 0))


use_random_boundaries = True
screen = pygame.display.set_mode((1000, 1000))
running = True
clock = pygame.time.Clock()
boundaries = []
if use_random_boundaries:
    random_boundaries()
else:
    tube()

v = Vector2D()
v.x = 100
v.y = 100
bag = Bag(v)
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    running = is_running(bag)
    bag.update_and_throw_balls(screen, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], boundaries,
                               clock.get_fps())
    for b in boundaries:
        b.draw(screen)
    pygame.display.flip()
