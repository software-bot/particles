import pygame


class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def reflect(self, v):
        v1 = pygame.math.Vector2()
        v1.x = self.x
        v1.y = self.y

        v2 = pygame.math.Vector2()
        v2.x = v.x
        v2.y = v.y

        v1 = v1.reflect(v2)
        return Vector2D(v1.x, v1.y)
