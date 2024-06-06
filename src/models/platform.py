import pygame, pygame.midi
from pygame import Vector2

from utils.midi import get_midi_out

class Platform(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int] | Vector2, 
        size: tuple[int, int] | Vector2,
        normal: tuple[float, float] | Vector2,
        note: int,
        color: tuple[int, int, int] = (255, 0, 0), 
    ):
        super().__init__()

        self.og_surf = pygame.Surface(size, pygame.SRCALPHA)
        self.og_rect = self.og_surf.get_rect(center=pos)
        w, h = size
        pygame.draw.rect(self.og_surf, color, (0, 0, w, h))

        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.normal = Vector2(normal).normalize()
        self.note = note
        self.color = color

        self.rotate_angle = 90 - self.normal.as_polar()[1]
        self.surf = pygame.transform.rotate(self.og_surf, self.rotate_angle)
        self.rect = self.surf.get_rect(center=self.og_rect.center)

        self.vel_out = Vector2(0, 0)
           
    def emit_note(self):
        get_midi_out().note_on(self.note, 64)
