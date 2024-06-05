import pygame, pygame.midi, sys, random
from pygame.locals import *
from pygame.math import Vector2
from utils import constants
from models.ball import Ball
from utils.sounds import parse_midi

pygame.init()
pygame.midi.init()

device_id = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(2)


clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Game")

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
B = Ball((50, 50), 10, color=(0, 255, 0), collides_with=platforms)
C = Ball((45, 700), 10)
all_sprites.add(B, C)
platforms.add(C)


note_timings = parse_midi("src/sounds/smb_over.mid", 1)
note_counter = 0
prev_platform = C

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    delta_time = clock.tick(constants.FPS) / 1000

    display_surface.fill((0, 0, 0))
    for entity in all_sprites:
        display_surface.blit(
            entity.surf,
            entity.pos - B.pos + (360, 640) - (entity.radius, entity.radius),
        )
    pygame.display.update()

    B.update(delta_time)
    if B.time_since_collision == 0:
        midi_out.note_on(note_timings[note_counter][0], 64)
        new_pos = B.predict_position(note_timings[note_counter][1])
        new_vel = B.predict_velocity(note_timings[note_counter][1])
        vel_ang = new_vel.as_polar()[1]
        bounce_ang = random.uniform(vel_ang - 30, vel_ang + 30)
        bounce_vec = Vector2.from_polar((19.5, bounce_ang))

        platforms.remove(prev_platform)
        prev_platform.color = (75, 0, 0)
        prev_platform.draw()
        platform = Ball(new_pos + bounce_vec, 10)
        all_sprites.add(platform)
        platforms.add(platform)

        prev_platform = platform
        note_counter += 1
