from mido import MidiFile


def ticks_to_seconds(ticks: int, tempo: int, ticks_per_beat: int):
    return (ticks * tempo) / (ticks_per_beat * 1_000_000)


def parse_midi(midi_path: str, track_ind: int) -> list[tuple[int, float]]:
    midi = MidiFile(midi_path)
    track = midi.tracks[track_ind]
    cur_ticks = 0
    cur_tempo = 0
    prev_note_ticks = None
    time_diffs = []

    for msg in track:
        cur_ticks += msg.time
        if msg.type == "set_tempo":
            cur_tempo = msg.tempo
        if msg.type == "note_on" and msg.velocity > 0:
            if prev_note_ticks is not None:
                tick_diff = cur_ticks - prev_note_ticks
                second_diff = ticks_to_seconds(
                    tick_diff, cur_tempo, midi.ticks_per_beat
                )
                time_diffs.append(second_diff)
            prev_note_ticks = cur_ticks

    time_diffs.append(9999)
    notes = [msg.note for msg in track if msg.type == "note_on"]
    return list(zip(notes, time_diffs))
