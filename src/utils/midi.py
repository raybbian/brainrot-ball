import pygame.midi
from mido import MidiFile

midi_out = None

def get_midi_out() -> pygame.midi.Output:
    if midi_out is None:
        return init_midi()

    return midi_out

def init_midi() -> pygame.midi.Output:
    global midi_out
    pygame.midi.init()
    midi_out = pygame.midi.Output(2)
    return midi_out

def parse_midi(midi_path: str, channel: int) -> list[tuple[int, float]]:
    midi = MidiFile(midi_path)
    cur_time = 0
    prev_note_time = None
    time_diffs = [1]
    notes = []

    for msg in midi:
        cur_time += msg.time
        if msg.type == "note_on" and msg.velocity > 0 and msg.channel == channel:
            notes.append(msg.note)
            if prev_note_time is not None:
                time_diff = cur_time - prev_note_time
                time_diffs.append(time_diff)
            prev_note_time = cur_time

    return list(zip(notes, time_diffs))

