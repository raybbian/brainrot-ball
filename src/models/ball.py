import pygame
from pygame import Vector2


class Ball(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int] | Vector2,
        vel: tuple[int, int] | Vector2,
        acc: tuple[int, int] | Vector2,
        radius: int,
        color: tuple[int, int, int] = (255, 0, 0),
    ):
        super().__init__()
        self.surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=pos)
        pygame.draw.circle(self.surf, color, (radius, radius), radius)

        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.acc = Vector2(acc)

        self.radius = radius
        self.color = color

    def set_pos(self, pos: tuple[int, int] | Vector2):
        self.pos = Vector2(pos)
        self.rect = self.surf.get_rect(center=self.pos)
