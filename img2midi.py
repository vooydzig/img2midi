import pygame, Image, argparse
from midiutil.MidiFile import MIDIFile
from itertools import groupby

A0_NOTE = 21
C8_NOTE = 108


def lerp(min, max, note):
  return int(min + note * (max - min))


def convert_rgb_to_note(r, g, b):
  return lerp(A0_NOTE, C8_NOTE, int((r+g+b)/6.0)/255.0)


def add_note(song, track, pitch, time, duration):
  song.addNote(track, 0, pitch, time, duration, 100)


def create_midi(tempo, data):
  print 'Converting to MIDI.'
  song = MIDIFile(1)
  song.addTempo(0, 0, tempo)

  grouped = [(note, sum(1 for i in g)) for note, g in groupby(data)]
  time = 0
  for note, duration in grouped:
    add_note(song, 0, note, time, duration)
    time += duration
  return song


def play_midi(music_file):
  clock = pygame.time.Clock()
  try:
    pygame.mixer.music.load(music_file)
    print "Music file %s loaded. Press Ctrl + C to stop playback." % music_file
  except Exception as e:
    print "Error loading file: %s - %s" % (music_file, e)
    return
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    clock.tick(30)


def get_song_data(filename):
  try:
    im = Image.open(filename).convert('RGB')
  except Exception as e:
    print "Error loading image: %s" % e
    raise SystemExit
  print "Img %s loaded." % filename
  w, h = im.size
  return [convert_rgb_to_note(*im.getpixel((x, y))) for y in range(h) for x in range(w)]


def convert(img_file, midi_file, play):
  pygame.init()
  data = get_song_data(img_file)
  song = create_midi(240, data)
  with open(midi_file, 'wb') as f:
    song.writeFile(f)

  if play:
    try:
      play_midi(midi_file)
    except KeyboardInterrupt:
      pygame.mixer.music.fadeout(1000)
      pygame.mixer.music.stop()
      raise SystemExit


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert image file to midi.')
  parser.add_argument('input', nargs=1, help='Path to input image file')
  parser.add_argument('output', nargs=1, help='Path to output midi file')
  parser.add_argument('--play', action='store_true', default=False, help='Play file after conversion')
  args = vars(parser.parse_args())

  convert(args['input'][0], args['output'][0], args['play'])
