from models.ball import Ball
from pygame import Vector2

from models.platform import Platform
from utils.midi import get_midi_out


MIN_SPEED = 500
BOUNCE_DECAY = 0.85

class LevelEvent():
    def __init__(
        self, 
        time: float,
        note: None | int,
        pos: tuple[int, int] | Vector2, 
        vel: tuple[int, int] | Vector2,
        acc: tuple[int, int] | Vector2 = Vector2(0, 981)
    ):
        self.time = time
        self.note = note
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.acc = Vector2(acc)


class LevelPlayer():
    def __init__(self, init_event: LevelEvent):
        self.timeline = [init_event]
        self.cur_time = 0
        self.prev_event_ind = 0
        self.next_event_ind = 1
        self.init_event = init_event

    def load_level(self, notes: list[tuple[int, float]]) -> list[Platform]:
        platforms = []
        fake_ball = Ball(self.init_event.pos, self.init_event.vel, self.init_event.acc, 10, color=(0, 255, 0))

        cur_time = 0
        current_dir = 1
        time_since_dir_change = 0

        for note, time_from_prev in notes:
            pos_when_play = fake_ball.pos + fake_ball.vel * time_from_prev + 0.5 * fake_ball.acc * time_from_prev**2
            vel_when_play = fake_ball.vel + fake_ball.acc * time_from_prev
            
            changed_dir = False
            time_since_dir_change += 1
            if len(platforms) > 0 and pos_when_play.y - platforms[-1].pos.y > 500 and time_since_dir_change > 5:
                current_dir *= -1
                changed_dir = True
                time_since_dir_change = 0

            vel_dir = vel_when_play.normalize()
            if not changed_dir:
                des_dir = Vector2(current_dir * 500 / vel_when_play.magnitude(), -1 if vel_when_play.y > 0 else 1).normalize()
            else:
                des_dir = Vector2(current_dir * 2000 / vel_when_play.magnitude(), -1 if vel_when_play.y < 0 else 1).normalize()
            bounce_dir = (vel_dir - (vel_dir + des_dir) / 2).normalize()

            platform = Platform(pos_when_play + bounce_dir * 15, (25, 10), bounce_dir, note)
            platforms.append(platform)
            
            new_vel = vel_when_play - 2 * vel_when_play.dot(bounce_dir) * bounce_dir
            if new_vel.magnitude() * BOUNCE_DECAY > MIN_SPEED:
                new_vel *= BOUNCE_DECAY
            
            bounce_event = LevelEvent(cur_time + time_from_prev, note, pos_when_play, new_vel)
            self.timeline.append(bounce_event)

            cur_time += time_from_prev
            fake_ball.pos = pos_when_play
            fake_ball.vel = new_vel

        self.init_playback()
        return platforms

    def init_playback(self):
        self.timeline = sorted(self.timeline, key=lambda x: x.time)
        self.cur_time = 0
        self.prev_event_ind = 0
        self.next_event_ind = 1

    def step_forward(self, delta_time: float) -> Vector2:
        self.cur_time += delta_time
        if self.timeline[self.next_event_ind].time < self.cur_time:
            prev_event = self.timeline[self.prev_event_ind]
            if prev_event.note is not None:
                get_midi_out().note_off(prev_event.note, 64)
            self.next_event_ind += 1
            self.prev_event_ind = self.next_event_ind - 1
            cur_event = self.timeline[self.prev_event_ind]
            if cur_event.note is not None:
                get_midi_out().note_on(cur_event.note, 64)

        prev_event = self.timeline[self.prev_event_ind]
        time_to_prev = self.cur_time - prev_event.time
        return prev_event.pos + prev_event.vel * time_to_prev + 0.5 * prev_event.acc * time_to_prev**2

    def get_init_event(self):
        return self.init_event


