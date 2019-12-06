"""For a detailed guide on all the features of the Circuit Playground Express (cpx) library:
https://adafru.it/cp-made-easy-on-cpx"""
import random
import time
import microcontroller
from adafruit_circuitplayground.express import cpx

# Set this as a float from 0 to 1 to change the brightness. The decimal represents a percentage.
# So, 0.3 means 30% brightness!
cpx.pixels.brightness = 0.2

# Changes to NeoPixel state will not happen without explicitly calling show()
cpx.pixels.auto_write = False
cpx.detect_taps = 1

tones = {
    'C': 262,
    'D': 294,
    'E': 330,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 494,
    'C2': 550,
}
notes = [
    ('E', .25),
    ('E', .25),
    ('E', .50),
    ('E', .25),
    ('E', .25),
    ('E', .50),
    ('E', .25),
    ('G', .50),
    ('C', .25),
    ('D', .25),
    ('E', .50),

    ('F', .25),
    ('F', .25),
    ('F', .25),
    ('F', .25),
    ('F', .25),
    ('E', .25),
    ('E', .50),

    ('E', .02),
    ('E', .02),
    ('G', .25),
    ('G', .25),
    ('F', .25),
    ('D', .25),
    ('C', 1.0),
    (None, 2.0),
]

note_index = 0
pixel_number = 0
shaken_count = 0
shook_up = 30
invert_colors = False
invert_direction = False
current_note = None
note_start = None
note_count = len(notes)
# time.monotonic() allows for non-blocking LED animations!
start = time.monotonic()
while True:
    now = time.monotonic()

    # If a shake is detected, turn on the snowglobe
    if cpx.shake(14):
        shaken_count = shook_up

    # Snowglobe mode
    if shaken_count > 0:
        shaken_count -= 1
        for white_pixel in range(10):
            how_shook = shaken_count / shook_up
            if how_shook > random.random():
                cpx.pixels[white_pixel] = tuple(int(255 * how_shook) for _ in range(3))
            else:
                cpx.pixels[white_pixel] = (0, 0, 0)
        cpx.pixels.show()

    # Wreath mode
    else:
        pixel_number = (pixel_number + 1) % 10
        useful_pixel_number = 9 - pixel_number if invert_direction else pixel_number
        cpx.pixels[useful_pixel_number] = (0, 255, 0) if invert_colors else (255, 0, 0)
        for p in range(1, 10):
            if invert_direction:
                pixel = useful_pixel_number - p
                pixel += 10 if pixel < 0 else 0
            else:
                pixel = (useful_pixel_number + p) % 10
            if invert_colors:
                cpx.pixels[pixel] = (int(225 * (p/40)), 0, 0)
            else:
                cpx.pixels[pixel] = (0, int(225 * (p/40)), 0)
            cpx.pixels.show()


    # Press the buttons to play sounds!
    if cpx.button_a:
        cpx.play_file("sound_a.wav")
        invert_colors = not invert_colors
    elif cpx.button_b:
        cpx.play_file("sound_b.wav")
        invert_direction = not invert_direction

    if cpx.tapped:
        new_brightness = cpx.pixels.brightness + .20
        if new_brightness > 1.0:
            new_brightness -= 1.0
        cpx.pixels.brightness = new_brightness


    # If the switch is to the left, it returns True!
    if cpx.switch:
        if current_note is None or now - note_start > current_note[1]:
            cpx.stop_tone()
            note_index = ( note_index + 1 ) % note_count
            current_note = notes[note_index]
            if current_note[0]:
                cpx.start_tone(tones[current_note[0]])
            note_start = now
    else:
        if current_note is not None:
            current_note = None
            cpx.stop_tone()
