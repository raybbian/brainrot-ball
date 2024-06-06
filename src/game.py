import pygame, pygame.midi, sys, random
from pygame import Vector2
from pygame.locals import *
from utils.level import LevelEvent, LevelPlayer
from utils.midi import parse_midi
from models.ball import Ball

pygame.init()

clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Game")

all_sprites = pygame.sprite.Group()

notes = parse_midi("src/sounds/smb_over.mid", 0)
init_state = LevelEvent(0, None, (50, 50), (0, 0))
playback = LevelPlayer(init_state)
platforms = playback.load_level(notes)
ball = Ball(init_state.pos, init_state.vel, init_state.acc, 10, (0, 255, 0))

all_sprites.add(ball, platforms)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    delta_time = clock.tick(165) / 1000

    display_surface.fill((0, 0, 0))
    for entity in all_sprites:
        display_surface.blit(
            entity.surf,
            Vector2(entity.rect.topleft) - Vector2(ball.rect.topleft) + Vector2(pygame.display.get_window_size()) / 2
        )
    pygame.display.update()

    ball.set_pos(playback.step_forward(delta_time))
