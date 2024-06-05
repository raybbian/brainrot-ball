from typing import Optional
import pygame
from pygame import Vector2


class Ball(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int] | Vector2,
        radius: int,
        color: tuple[int, int, int] = (255, 0, 0),
        collides_with: Optional[pygame.sprite.Group] = None,
    ):
        super().__init__()
        self.surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 981)

        self.color = color
        self.radius = radius
        self.collides_with = collides_with
        self.time_since_collision = 0
        self.size = Vector2(radius * 2, radius * 2)

        self.draw()

    def draw(self):
        pygame.draw.circle(
            self.surf, self.color, (self.radius, self.radius), self.radius
        )

    def move(self, delta_time: float):
        self.vel += self.acc * delta_time
        self.pos += self.vel * delta_time

    def check_collision(self, other) -> bool:
        return self.pos.distance_to(other.pos) < self.radius + other.radius

    def resolve_collision(self, other):
        normal_dir = (self.pos - other.pos).normalize()
        # https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector
        self.vel = self.vel - 2 * self.vel.dot(normal_dir) * normal_dir
        self.vel *= 0.95

    def update(self, delta_time: float):
        self.time_since_collision += delta_time

        if (
            self.collides_with is not None
            and self.time_since_collision > 2 * delta_time
        ):
            for obj in self.collides_with:
                if self.check_collision(obj):
                    self.resolve_collision(obj)
                    self.time_since_collision = 0

        self.move(delta_time)

    def predict_position(self, s_from_now: float) -> Vector2:
        return self.pos + self.vel * s_from_now + 0.5 * self.acc * s_from_now**2

    def predict_velocity(self, s_from_now: float) -> Vector2:
        return self.vel + self.acc * s_from_now
