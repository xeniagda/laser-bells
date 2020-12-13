import mido

ON_THRESHOLD = 40

def midi_note_to_freq(note):
    # A4 = 69mid = 440Hz
    return 440 * 2 ** ((note - 69) / 12)

def track_to_timestamps(track, channel, time_scale):
    t = 0
    out = [] # [(freq, time)]
    for msg in track:
        if msg.type == "note_on" and msg.channel == channel:
            t += msg.time
            print(msg)

            if msg.velocity > ON_THRESHOLD:
                freq = midi_note_to_freq(msg.note)
            else:
                freq = 0

            out.append((t * time_scale, freq))

    return out

def read_midi(file_to_parse):

    file_to_parse = "MIDI-Samples/Jingle_Bells.mid"

    mid = mido.MidiFile(file_to_parse)

    track = mid.tracks[0]


    return track_to_timestamps(track, 0, 1 / mid.ticks_per_beat)
