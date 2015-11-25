img2midi
==

You too can be a synesthete!
With this python script You can create simple melodies, or cacophonies, from images.
Yes, it means You can actualy **head** the images. 


Requirements
--
* PIL
* pygame - only for playing final midi song
* midiUtil: [https://code.google.com/p/midiutil/](https://code.google.com/p/midiutil/)


Usage
--
1. Clone or download
2. In cmd type: `python img2midi.py input.jpg song.midi --play`
3. Enjoy

`input` and `output` are required to run script, play flag is optional. Script will create midi file. **Please note:** The larger the input image file the longer final song will be.


Math behind the conversion
--
Converter uses naive way of converting pixel colors to midi notes. Each pixel's color consists of RGB components and each of those components has a value in range [0; 255]. Midi notes can take any value from 21 - A0 note(low A, 0th octave), to 108 - C8 (high C, 8th octave) note, therefore conversion between those ranges must be made. For simplicity I arbitrarily decided that, final song's tempo will be 240 BPM.

Color to pitch conversion is made using following algorithm for every pixel:

1. Take average of RGB color components of a pixel. This will be value in range (0; 255)
2. Divide it by 2, this value was arbitrarily decided, so that final notes will be less spread out on a scale
3. Normalize it by dividing by 255
4. Using linear interpolation convert normalized pixel value to note.
5. This is a final midi note value in range [21; 108]

Base note duration was chosen to be 1 beat. However if the same value is repeated in the final song data 1 beat is added for each repetition.

Example:

`[50, 50, 50, 80, 40, 40, 50, 50]` will result in 4 notes:

* D3(50) with duration of 3 beats
* G#5(80) with duration of 1 beat
* E2(40) with duration of 2 beats
* D3(50) with duration of 2 beats