from midiutil import MIDIFile

bpm = 60
time_signature = (4, 4)

track = 0
channel = 0

midi = MIDIFile(1)

midi.addTempo(track, 0, bpm)
midi.addTimeSignature(track, 0, *time_signature, 24)

melody = [(48, 80, 1), (51, 80, 1), (55, 80, 2), (44, 80, 1), (48, 80, 1), (52, 80, 1), (55, 80, 1), (59, 80, 1), (52, 60, 2), (57, 100, 1), (53, 80, 1), (55, 100, 1), (49, 70, 2), (45, 80, 2), (49, 50, 2), (40, 120, 1), (45, 120, 1), (56, 120, 1), (63, 120, 1), (60, 120, 1), (71, 120, 1), (69, 80, 2), (65, 80, 1), (59, 70, 1), (55, 75, 1), (52, 70, 1), (51, 80, 1), (60, 70, 1), (76, 120, 2), (65, 87, 1), (70, 88, 1), (62, 95, 1), (55, 90, 1), (56, 87, 2), (60, 84, 2)]

time = 0
for note in melody:
    pitch, velocity, duration = note
    midi.addNote(track, channel, pitch, time, duration, velocity)
    time += duration

with open("simple_melody2.mid", "wb") as output_file:
    midi.writeFile(output_file)
