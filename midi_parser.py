import mido

ON_THRESHOLD = 40

def midi_note_to_freq(note):
    # A4 = 69mid = 440Hz
    return 440 * 2 ** ((note - 69) / 12)

def track_to_timestamps(track, channel, time_scale, use_min):
    t = 0
    out = [] # [(freq, time)]

    current_note = -1

    for msg in track:
        if msg.type == "note_on" and (msg.channel == channel or channel == -1):
            t += msg.time

            if msg.velocity > ON_THRESHOLD:
                if ((msg.note < current_note) != use_min) or current_note == -1:
                    freq = midi_note_to_freq(msg.note)
                    current_note = msg.note
                else:
                    continue
            else:
                if msg.note == current_note:
                    freq = 0
                    current_note = -1
                else:
                    continue

            out.append((t * time_scale, freq))

    return out

def read_midi(file_to_parse, track, channel, use_min, ts):
    mid = mido.MidiFile(file_to_parse)

    track = mid.tracks[track]

    return track_to_timestamps(track, channel, (1 / ts) / mid.ticks_per_beat, use_min)
