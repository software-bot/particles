import pygame


class Boundary:
    def __init__(self, start, end, angle):
        self.start = start
        self.end = end
        self.color = (60, 60, 60)
        self.angle = angle

    def draw(self, screen):
        pygame.draw.line(screen, self.color,
                         (self.start.x, self.start.y),
                         (self.end.x, self.end.y), 2)
